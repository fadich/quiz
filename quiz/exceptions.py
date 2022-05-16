__all__ = [
    "QuizError",
    "HandlerError",
    "OptionError",
    "ParsingError",
]


class QuizError(Exception):
    pass


class HandlerError(QuizError):
    pass


class OptionError(QuizError, KeyError):
    pass


class ParsingError(QuizError, TypeError):
    pass
