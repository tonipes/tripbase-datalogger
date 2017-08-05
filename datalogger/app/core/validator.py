import logging

from .exception import ValidationError

_logger = logging.getLogger(__name__)


class Validator(object):
    def __init__(self, constraint=None):
        self.constraint = constraint
        pass

    @staticmethod
    def _raise(msg, info):
        raise ValidationError(msg, info)

    @staticmethod
    def _add_to_path(path, key):
        form = "{}.{}"
        if not path:
            form = "{}{}"
        if isinstance(key, int):
            form = "{}[{}]"

        return form.format(path, key)

    def _check_constraint(self, path, casted_key):
        if self.constraint and casted_key is not None:
            try:
                self.constraint(casted_key)
            except (ValueError, AssertionError) as err:
                self._raise(
                    "Validation error: '{}' fails validation".format(path),
                    "{}".format(err)
                )

    def _get_casted(self, t, path, val):
        try:
            return t(val)
        except (ValueError, TypeError):
            self._raise(
                "Invalid cast to {} at {}".format(t.__name__, path),
                "Cannot cast '{}' to '{}'".format(val, t.__name__)
            )

    def validate(self, path, val):
        pass


class LineValidator(Validator):
    def __init__(self, t=None, constraint=None, default=None):
        super(LineValidator, self).__init__()
        self.T = t
        self.constraint = constraint
        self.default = default

    def validate(self, path, val):
        super(LineValidator, self).validate(path, val)
        value = val

        if self.T:
            value = self._get_casted(self.T, path, val)

        self._check_constraint(path, value)

        return value
#
#
# class ListValidator(Validator):
#     def __init__(self, validator, default=None):
#         super(ListValidator, self).__init__()
#         self.validator = validator
#         self.default = default  # if default is not None else []
#
#     def validate(self, path, val):
#         super(ListValidator, self).validate(path, val)
#         if val and not isinstance(val, list):
#             self._raise(
#                 "Value at '{}' needs to be list".format(path),
#                 ""
#             )
#
#         res = []
#         if val:
#             for i, item in enumerate(val):
#                 res.append(self.validator.validate(
#                     self._add_to_path(path, i),
#                     item
#                 ))
#
#         return res


class SchemaValidator(Validator):
    def __init__(self, values=None, default=None):
        super(SchemaValidator, self).__init__()
        self.values = values if values else {}
        self.default = default  # if default is not None else {}

    def validate(self, path, val_tuple):
        super(SchemaValidator, self).validate(path, val_tuple)
        if not isinstance(val_tuple, dict):
            self._raise("Value at '{}' needs to be dict".format(path), "")

        res = {}
        for k, v in self.values.items():
            p = self._add_to_path(path, k)
            if k in val_tuple:
                res[k] = self.values[k][0].validate(
                    p,
                    val_tuple[k] if k in val_tuple else None,
                )
            elif not self.values[k][1]:
                res[k] = v[0].default
            else:
                self._raise(
                        "Missing required field: '{}'".format(p),
                        ""
                    )

        return res
