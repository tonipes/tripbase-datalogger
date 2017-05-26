import datetime
import logging

from .core.schema import *
from .core.exception import ValidationError
from .core.validator import LineValidator, ListValidator, SchemaValidator

_logger = logging.getLogger(__name__)

# DATE_FORMAT = '%Y%m%d%H%M%S'
LAT_LIMIT = 85.05112878
LNG_LIMIT = 180

######################
# Validation helpers #
######################


def validate_date(val: str) -> bool:
    pass
    # try:
    #     datetime.datetime.strptime(val, DATE_FORMAT)
    # except ValueError:
    #     raise ValidationError(
    #         "Incorrect date format",
    #         "Should be '{}', is '{}'".format(DATE_FORMAT, val)
    #     )


def lat_long_validation(val: float, limit: float):
    if not -limit <= val <= limit:
        raise ValidationError(
            "Value is outside it's range",
            "'{} <= {} <= {}'".format(-limit, val, limit)
        )


def validate_lat(val: float) -> bool:
    lat_long_validation(val, LAT_LIMIT)


def validate_long(val: float) -> bool:
    lat_long_validation(val, LNG_LIMIT)


################
# Schema stuff #
################


EpochDateTime = LineValidator(int, lambda v: validate_date(v))
LatitudeLine = LineValidator(float, lambda v: validate_lat(v))
LongitudeLine = LineValidator(float, lambda v: validate_long(v))
