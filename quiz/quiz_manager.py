__all__ = [
    "QuizManager",
]

import random

from collections import OrderedDict
from typing import Iterable, Dict, Callable, List

from .exceptions import OptionError, HandlerError
from .models import Question, Option


class QuizManager:

    def __init__(
        self,
        questions: Iterable[Question],
        handlers: Dict[str, Callable],
    ):
        self._handlers = handlers
        self._queued_questions = list(questions)

        self._validate_handlers()

        self._options = {}
        self._question_list = []
        self._triggers = set()

    def __iter__(self):
        return self

    def __next__(self) -> str:
        self._load_questions()
        if not self._question_list:
            raise StopIteration()

        random.shuffle(self._question_list)

        question = self._question_list.pop()

        options = list(question.options)
        random.shuffle(options)

        self._load_options(options)

        return question.title

    def get_options(self):
        options = OrderedDict()
        for key in sorted(map(int, self._options.keys())):
            options[str(key)] = self._options[str(key)].title

        return options

    def select_option(self, key: str) -> Option:
        if key not in self._options:
            raise OptionError(f"No option \"{key}\" found")

        option: Option = self._options[key]

        self._triggers |= set(option.triggers)
        for action in option.callbacks:
            self._handlers[action]()

        return option

    def _validate_handlers(self):
        for question in self._queued_questions:
            for option in question.options:
                for callback in option.callbacks:
                    if callback not in self._handlers:
                        raise HandlerError(
                            f"No handler <{callback}> found for option \"{option.title}\" of "
                            f"question \"{question.title}\""
                        )

    def _load_questions(self):
        remaining_questions = []

        for question in self._queued_questions:
            if question.condition.satisfied(self._triggers):
                self._question_list.append(question)
                continue

            remaining_questions.append(question)

        self._queued_questions = remaining_questions

    def _load_options(self, options: List[Option]):
        self._options = {str(i + 1): options[i] for i in range(len(options))}

