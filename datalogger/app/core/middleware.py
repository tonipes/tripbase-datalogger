import falcon
import logging
import json
import uuid

_logger = logging.getLogger(__name__)


class Middleware(object):
    def __init__(self, db_engine):
        super(Middleware, self).__init__()
        self.db_engine = db_engine

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource, params):
        pass

    def process_response(self, req, resp, resource):
        pass


class RequestContextMiddleware(Middleware):
    def process_request(self, req, resp):
        req.context['uuid'] = str(uuid.uuid4())
        req.context['db'] = self.db_engine.get_db()


class JsonRequestMiddleware(Middleware):
    """ Parses request body to json object
        Json object can be found in context """

    def _get_body_string(self, stream):
        s = ""
        for line in stream:
            s += line.decode("utf-8")
        return s

    def process_resource(self, req, resp, resource, params):
        content_type = req.get_header('Content-Type')

        if content_type and 'json' in content_type:
            body_string = ""
            try:
                body_string = self._get_body_string(req.stream)
                body_obj = json.loads(body_string)
            except Exception as e:
                _logger.warning('Invalid JSON in request', extra={
                    'data': {
                        'error': e,
                        'request': req.env,
                        'context': req.context,
                        'body': body_string,
                    }
                })
                raise falcon.HTTPBadRequest('Invalid JSON', 'Please provide valid JSON')

            req.context['body_obj'] = body_obj

        else:
            raise falcon.HTTPBadRequest('Invalid Format', 'Please provide data in JSON Format')


class JsonResponseMiddleware(Middleware):
    """ Translated result from context to json string body"""

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])
        resp.append_header('Content-Type', 'application/json')


class AuthMiddleware(Middleware):
    """ Checks if request has valid api key.
        Raises HTTP Unauthorized exception if valid api key is not found """

    def __init__(self, db_engine, apikeys):
        super(AuthMiddleware, self).__init__(db_engine)
        self.keys = apikeys

    def _token_is_valid(self, token):
        return token in self.keys

    def process_resource(self, req, resp, resource, params):
        if req.method not in ['OPTIONS']:
            # params = dict(urllib.parse.parse_qsl(req.query_string))
            # token = params.get('apikey', None)
            token = req.auth

            if token is None:
                _logger.warning('Unauthorized request. No token given.', extra={
                    'data': {'request': req.env, 'context': req.context}
                })
                raise falcon.HTTPUnauthorized(
                    'Authentication required',
                    'Please provide an API key as part of the request.', []
                )

            if not self._token_is_valid(token):
                _logger.warning('Unauthorized request. Invalid token.', extra={
                    'data': {'request': req.env, 'context': req.context}
                })
                raise falcon.HTTPUnauthorized(
                    'Authentication failed',
                    'The provided API key is not valid.', []
                )
