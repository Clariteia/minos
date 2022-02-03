import pathlib
import unittest
from unittest.mock import (
    call,
    patch,
)

import yaml

from minos.cli import (
    Form,
    Question,
)


class TestForm(unittest.TestCase):
    def setUp(self) -> None:
        self.questions = [
            Question("foo", "int"),
            Question("bar", "str", link=True),
        ]
        self.form = Form(self.questions)

    def tearDown(self) -> None:
        answers_file_path = pathlib.Path.cwd() / ".minos-answers.yml"
        if answers_file_path.exists():
            answers_file_path.unlink()

    def test_constructor(self):
        self.assertIsInstance(self.form, Form)
        self.assertEqual(self.questions, self.form.questions)

    def test_from_raw(self):
        raw = {"questions": [{"name": "foo", "type": "int"}, {"name": "bar", "type": "str", "link": True}]}
        observed = Form.from_raw(raw)
        self.assertEqual(self.form, observed)

    def test_links(self):
        self.assertEqual(["bar"], self.form.links)

    def test_ask(self):
        with patch("minos.cli.Question.ask", side_effect=["one", "two"]) as mock:
            observed = self.form.ask()

        self.assertEqual({"foo": "one", "bar": "two"}, observed)
        self.assertEqual([call(context=observed), call(context=observed)], mock.call_args_list)

    def test_form_with_previous_answers(self):
        answers_file_path = pathlib.Path.cwd() / ".minos-answers.yml"
        with answers_file_path.open("a") as answers_file:
            yaml.dump({"foo": "foo_answer", "bar": "bar_answer"}, answers_file)

        with patch("minos.cli.Question.ask", side_effect="bar") as mock:
            observed = self.form.ask()
            self.assertEqual({"foo": "foo_answer", "bar": "bar_answer"}, observed)

        self.assertEqual(0, mock.call_count)

    def test_form_without_previous_answers(self):
        answers_file_path = pathlib.Path.cwd() / ".minos-answers.yml"

        with patch("minos.cli.Question.ask", return_value="resp") as mock:
            observed = self.form.ask()
            self.assertEqual({"foo": "resp", "bar": "resp"}, observed)

        self.assertEqual(2, mock.call_count)

        with answers_file_path.open("r") as answers_file:
            answers = yaml.safe_load(answers_file)
            self.assertEqual({"foo": "resp", "bar": "resp"}, answers)


if __name__ == "__main__":
    unittest.main()
