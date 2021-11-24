from __future__ import (
    annotations,
)

from typing import (
    Any,
    Optional,
)

from ..console import (
    console,
)


class Question:
    """TODO"""

    def __init__(self, name: str, type_: str, help_: Optional[str], choices: Optional, default: Optional):
        self.name = name
        self.type_ = type_
        self.help_ = help_
        self.choices = choices
        self.default = default

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Question:
        """TODO"""
        return cls(
            name=raw.get("name"),
            type_=raw.get("type", None),
            help_=raw.get("help", None),
            choices=raw.get("choices", None),
            default=raw.get("default", None),
        )

    def ask(self) -> str:
        """TODO"""
        answer = console.input(self.title)
        if answer == "":
            answer = self.default
        return answer

    @property
    def title(self) -> str:
        """TODO"""
        title = str()
        if self.help_ is not None:
            title += self.help_
        else:
            title += self.name

        if self.default is not None:
            title += f" [ {self.default!r} ]"

        title += '\n'
        return title
