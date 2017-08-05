from .exception import FieldNotFoundError
from .validator import Validator, LineValidator

fields = {}


def get_field(name):
    if name in fields:
        return fields[name]
    else:
        raise FieldNotFoundError("Field '{}' not found!".format(name))


class Field(object):
    def __init__(self, name, validator: Validator=None, required=False):
        self.name = name
        self.required = required
        self.validator = validator


fields['base.float'] = Field('base.float', LineValidator(float))
fields['base.int'] = Field('base.int', LineValidator(int))
fields['base.text'] = Field('base.text', LineValidator(str))
