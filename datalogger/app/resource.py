import logging

from .core import resource
from .core.validator import LineValidator, ListValidator, SchemaValidator
from . import schema

_logger = logging.getLogger(__name__)

LOCATION_LOG_VALIDATOR = SchemaValidator({
    'timestamp': (schema.EpochDateTime, True),
    'latitude':  (schema.LatitudeLine,  True),
    'longitude': (schema.LongitudeLine, True),
    'test':      (schema.Text, False),
})

QUERY_VALIDATOR = SchemaValidator({
    'query': (schema.QueryList, True),
    'read':  (schema.KeyList,   True),
})


class LocationLogResource(resource.SchemaResource):
    _name = 'res_location_log'
    _data_schema = LOCATION_LOG_VALIDATOR
    _query_schema = QUERY_VALIDATOR
