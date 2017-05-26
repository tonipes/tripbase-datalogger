from .validator import LineValidator, ListValidator, SchemaValidator
from .exception import ValidationError
from . import search


def validate_query_combine_operator(val):
    if val not in search.COMBINE_OPERATORS:
        raise ValidationError(
            "Invalid combine operator in query",
            "Should be one of '{}', is '{}'".format(search.COMBINE_OPERATORS, val)
        )


def validate_query_domain(val):
    if len(val) != 3:
        raise ValidationError(
            "Invalid length of comparison in query",
            "Should be 3, is '{}'".format(len(val))
        )
    elif val[1] not in search.COMPARISON_OPERATORS:
        raise ValidationError(
            "Invalid operation in comparison",
            "Should be one of '{}', is '{}'".format(search.COMPARISON_OPERATORS, val[1])
        )


def validate_query(val):
    if isinstance(val, list):
        validate_query_domain(val)
    elif isinstance(val, str):
        validate_query_combine_operator(val)
    else:
        raise ValidationError(
            "Invalid member in query",
            "Should be either list or string, is '{}'".format(type(val).__name__)
        )


def validate_method(val: str):
    methods = ['create', 'query']
    if val not in methods:
        raise ValidationError(
            "Unsupported method",
            "Should be some of {}, is '{}'".format(methods, val)
        )

Text = LineValidator(str)
Float = LineValidator(float)
Int = LineValidator(int)

IntList = ListValidator(Int)

Key = LineValidator(str)
KeyList = ListValidator(Key)

Query = LineValidator(None, lambda v: validate_query(v))
QueryList = ListValidator(Query)

Method = LineValidator(str, lambda v: validate_method(v))
