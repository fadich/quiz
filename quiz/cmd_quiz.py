from collections import OrderedDict

from .exceptions import OptionError
from .quiz_manager import QuizManager


class CmdQuiz:

    def __init__(self, quiz_manager: QuizManager):
        self._quiz = quiz_manager

    def start_quiz(self):
        try:
            for question in self._quiz:
                self._pre_iteration()
                self._show_question(question)
                self._show_options(self._quiz.get_options())
                self._select_option()
                self._post_iteration()
        except KeyboardInterrupt:
            pass

    def _show_question(self, title: str):
        print(title)

    def _show_options(self, options: OrderedDict):
        for key, option in options.items():
            self._show_option(key, option)

    def _show_option(self, key: str, title: str):
        print(f"{key}. {title}")

    def _select_option(self):
        while True:
            option_key = self._read_option()

            try:
                option = self._quiz.select_option(key=option_key)
                self.print(option.title)
            except OptionError:
                self._show_option_error(key=option_key)
            else:
                break

    def _read_option(self) -> str:
        return input("> ")

    def _pre_iteration(self):
        self.print("")

    def _post_iteration(self):
        self.print("")

    def _show_option_error(self, key):
        self.print(f"No option \"{key}\" found")

    def print(self, line: str = ""):
        print(u"{line}".format(line=line))
