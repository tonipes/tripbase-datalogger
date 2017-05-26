import logging

_logger = logging.getLogger(__name__)


class ValidationError(Exception):
    def __init__(self, message, info=None):
        super(ValidationError, self).__init__(message)
        self.info = info
        self.message = message


class ResourceDefinitionError(Exception):
    def __init__(self, message):
        super(ResourceDefinitionError, self).__init__(message)
