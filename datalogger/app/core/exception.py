import logging

_logger = logging.getLogger(__name__)

class TBError(Exception):
    def __init__(self, message, info=None):
        super(TBError, self).__init__(message)
        self.info = info
        self.message = message


class ValidationError(TBError):
    pass


class ResourceDefinitionError(TBError):
    pass


class ModelNotFoundError(TBError):
    pass

class FieldNotFoundError(TBError):
    pass