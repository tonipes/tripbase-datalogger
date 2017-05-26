import logging

_logger = logging.getLogger(__name__)

class Sink(object):
    def __init__(self):
        pass

    @staticmethod
    def get_sink(self, req, resp):
        _logger.debug("Request went to sink")