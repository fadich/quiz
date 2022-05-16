__all__ = [
    "Condition",
    "Option",
    "Question",
]

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Condition:
    condition: Iterable[str]
    operator: str

    AND_OPERATORS = (
        "&",
        "&&",
        "and",
        "all",
    )

    OR_OPERATORS = (
        "|",
        "||",
        "or",
        "any",
        "one",
        "one of"
    )

    def satisfied(self, actions: Iterable[str]):
        if not self.condition:
            return True

        if self.operator in self.AND_OPERATORS:
            return not (set(self.condition) ^ set(actions))

        return bool(set(self.condition) & set(actions))

    def __str__(self):
        if not self.condition:
            return "*"

        if self.operator in self.AND_OPERATORS:
            oper = "&&"
        else:
            oper = "||"

        return f" {oper} ".join(self.condition)


@dataclass
class Option:
    title: str
    triggers: Iterable[str]
    callbacks: Iterable[str]

    def __str__(self):
        return f"{self.title} (triggers: [{', '.join(self.triggers)}]; actions: [{', '.join(self.callbacks)}])"


@dataclass
class Question:
    title: str
    options: Iterable[Option]
    condition: Condition

    def __str__(self):
        return f"{self.title} (condition: <{str(self.condition)}>; options: {', '.join(map(str, self.options))})"
