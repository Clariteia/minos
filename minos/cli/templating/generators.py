from pathlib import (
    Path,
)
from typing import (
    Any,
    Union,
)

from cached_property import (
    cached_property,
)
from copier import (
    copy,
)
# noinspection PyProtectedMember
from copier.config.factory import (
    filter_config,
)
from copier.config.objects import (
    EnvOps,
)
from copier.config.user_data import (
    load_config_data,
)
# noinspection PyProtectedMember
from copier.tools import (
    get_jinja_env,
)
from jinja2 import (
    Environment,
)

from ..consoles import (
    console,
)
from ..wizards import (
    Form,
)
from .fetchers import (
    TemplateFetcher,
)


class TemplateProcessor:
    """Template Processor class.

    This class generates a scaffolding structure on a given directory.
    """

    def __init__(self, source: Path, target: Path):
        self.source = source
        self.target = target

    @classmethod
    def from_fetcher(cls, fetcher: TemplateFetcher, target: Path):
        """TODO

        :param fetcher:
        :param target:
        :return:
        """
        return cls(fetcher.path, target)

    @property
    def destination(self) -> Path:
        """Get the location of the rendered template.

        :return: A ``Path`` instance.
        """
        return self.target.parent

    @cached_property
    def answers(self) -> dict[str, Any]:
        """Get the answers of the form.

        :return: A mapping from question name to the answer value.
        """
        return self.form.ask(env=self.env)

    @cached_property
    def form(self) -> Form:
        """Get the form.

        :return: A ``Form`` instance.
        """
        questions = list()
        for name, question in filter_config(self._config_data)[1].items():
            if name == "name" and question.get("default", None) is None:
                question["default"] = self.target.name
        return Form.from_raw({"questions": questions})

    @cached_property
    def env(self) -> Environment:
        """Get the Jinja's environment.

        :return:
        """
        return get_jinja_env(EnvOps(**self._config_data.get("_envops", {})))

    @cached_property
    def _config_data(self):
        return load_config_data(self.source)

    def render(self, **kwargs) -> None:
        """Performs the template building.

        :param kwargs: Additional named arguments.
        :return: This method does not return anything.
        """
        if not self.target.exists():
            self.target.mkdir(parents=True, exist_ok=True)

        if not self.target.is_dir():
            raise ValueError(f"{self.target!r} is not a directory!")

        self.render_copier(self.source, self.destination, self.answers, **kwargs)

    @staticmethod
    def render_copier(
        source: Union[Path, str], destination: Union[Path, str], answers: dict[str, Any], **kwargs
    ) -> None:
        """Render a template using ``copier`` as the file orchestrator.

        :param source: The template path.
        :param destination: The destination path.
        :param answers: The answers to the template questions.
        :param kwargs: Additional named arguments.
        :return: This method does not return anything.
        """
        if not isinstance(source, str):
            source = str(source)
        if not isinstance(destination, str):
            destination = str(destination)
        with console.status("Rendering template...", spinner="moon"):
            copy(src_path=source, dst_path=destination, data=answers, quiet=True, **kwargs)
        console.print(":moon: Rendered template!\n")
