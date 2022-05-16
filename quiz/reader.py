__all__ = [
    "from_json",
    "from_yaml",
    "from_dict",
]

import json

from typing import List, Dict, Any, Iterable

import yaml

from .exceptions import ParsingError
from .models import (
    Question,
    Condition,
    Option,
)


def validate_non_empty_string(value: Any, error_msg: str):
    if not isinstance(value, str) or not len(value):
        raise ParsingError(error_msg)

    return value


def validate_non_empty_list(value: Any, error_msg: str):
    if not isinstance(value, list) or not len(value):
        raise ParsingError(error_msg)

    return value


def validate_list_of_strings(value: Any, non_list_error: str, non_string_item_error: str):
    if value is None:
        value = []
    if isinstance(value, str):
        value = [value, ]

    if not isinstance(value, List):
        raise ParsingError(non_list_error)

    all(map(lambda x: validate_non_empty_string(x, non_string_item_error), value))

    return value


def from_json(filename: str, **file_params):
    with open(filename, "r", **file_params) as file:
        return from_dict(json.loads(file.read()))


def from_yaml(filename: str, **file_params):
    with open(filename, "r", **file_params) as file:
        return from_dict(yaml.safe_load(file) or {})


def from_dict(raw_data: Dict[str, Any]) -> Iterable[Question]:
    questions = []

    # Prepare data
    for question, opts in raw_data.items():
        condition = opts.pop("__condition__", None)
        condition_operator = opts.pop("__condition_operator__", None)

        options = []
        for opt, params in opts.items():
            if params is None:
                params = {}

            if not isinstance(params, dict):
                raise ParsingError(f"Question Option should be a dict, {repr(params)} given for Option \"{opt}\"")

            options.append({
                "title": opt,
                "callbacks": params.get("__callbacks__"),
                "triggers": params.get("__triggers__"),
            })

        questions.append({
            "title": question,
            "options": options,
            "condition": condition,
            "condition_operator": condition_operator,
        })

    validate_non_empty_list(
        value=questions,
        error_msg="No questions found"
    )

    # Validate and init Questions
    for question in questions:
        title = question.get("title")
        cond = question.get("condition")
        opts = question.get("options")
        cond_oper = question.get("condition_operator")

        validate_non_empty_string(
            value=title,
            error_msg=f"Question Title should be non-empty string, {repr(title)} given"
        )

        opts = validate_non_empty_list(
            value=opts,
            error_msg=f"Question should has at least one Option, no options given"
        )

        options = []
        for opt in opts:
            if isinstance(opt, str):
                opt = {
                    "title": opt,
                }

            opt_title = opt.get("title")
            opt_callbacks = opt.get("callbacks")
            opt_triggers = opt.get("triggers")

            opt_title = validate_non_empty_string(
                value=opt_title,
                error_msg=f"Question Option Title should be non-empty string, {repr(opt_title)} given"
            )

            opt_callbacks = validate_list_of_strings(
                value=opt_callbacks,
                non_list_error=f"Question Option Callbacks should be a List, {repr(opt_callbacks)} given",
                non_string_item_error=f"Question Option Callbacks items should be non-empty string"
            )

            opt_triggers = validate_list_of_strings(
                value=opt_triggers,
                non_list_error=f"Question Option Triggers should be a List, {repr(opt_triggers)} given",
                non_string_item_error=f"Question Option Triggers items should be non-empty string"
            )

            option = Option(
                title=opt_title,
                callbacks=opt_callbacks,
                triggers=opt_triggers,
            )

            options.append(option)

        cond = validate_list_of_strings(
            value=cond,
            non_list_error=f"Question Condition should be a List, {repr(cond)} given",
            non_string_item_error=f"Question Condition items should be non-empty string"
        )

        allowed_operators = Condition.AND_OPERATORS + Condition.OR_OPERATORS
        if cond_oper is None:
            cond_oper = Condition.OR_OPERATORS[0]

        cond_oper = cond_oper.lower()
        if cond_oper not in allowed_operators:
            raise ParsingError(
                f"Question Condition Operator should be one of {allowed_operators}, {repr(repr)} given"
            )

        condition = Condition(
            condition=cond,
            operator=cond_oper,
        )

        yield Question(
            title=title,
            options=options,
            condition=condition
        )
