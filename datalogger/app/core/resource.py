import logging
import redis

_logger = logging.getLogger(__name__)


class ModelResource(object):
    _resources = []

    def __init__(self, db_engine, resources=None):
        self.resources = resources if resources else []
        self.db_engine = db_engine

    def _register_resource(self, name, resource_obj):
        pass

    def query(self, r: redis.Redis, req, resp, obj, **kwargs):
        pass

    def create(self, r: redis.Redis, req, resp, obj, **kwargs):
        pass

    def query(self, r: redis.Redis, req, resp, data):
        print(data)
        pass
        # self.db_engine.query(self._name, obj, r)

    def create(self, r: redis.Redis, req, resp, data):
        print(data)
        pass
        # self.db_engine.create(self._name, obj, r)

    def on_post(self, req, resp, **kwargs):
        print(kwargs)
        body = req.context['body_obj']
        r = req.context['db']
        validated_body = self._validate('', body, req, self._body_base_fields)
        method = validated_body['method']

        if method == 'create':
            self.create(r, req, resp, **kwargs)

        elif method == 'query':
            self.query(r, req, resp, **kwargs)


# class SchemaResource(Resource):
#     _body_base_fields = SchemaValidator({
#         'method': (schema.Method, True),
#     })
#
#     _data_schema = None
#     _query_schema = None
#
#     def __init__(self, r):
#         super(SchemaResource, self).__init__(r)
#
#     @staticmethod
#     def _validate(path, obj, req, validation_schema):
#         if not validation_schema:
#             return obj
#
#         try:
#             validated = validation_schema.validate(path, obj)
#             return validated
#
#         except ValidationError as e:
#             _logger.error(
#                 "Schema validation error: {}".format(e.message),
#                 extra={
#                     'data': {
#                         'error_message': e.message,
#                         'error_info': e.info,
#                         'request': req.env,
#                         'context': req.context,
#                         'schema': type(validation_schema).__name__,
#                         'body': obj,
#                     }
#                 }
#             )
#             _logger.debug(e.info)
#
#             raise falcon.HTTPBadRequest(
#                 "Schema validation error", "{}.{}".format(
#                     e.message,
#                     " " + e.info if e.info else ''
#                 )
#             )
#
#     def query(self, r: redis.Redis, req, resp, obj, **kwargs):
#         self.db_engine.query(self._name, obj, r)
#
#     def create(self, r: redis.Redis, req, resp, obj, **kwargs):
#         self.db_engine.create(self._name, obj, r)
#
#     def on_post(self, req, resp, **kwargs):
#         body = req.context['body_obj']
#         r = req.context['db']
#         validated_body = self._validate('', body, req, self._body_base_fields)
#         method = validated_body['method']
#
#         if method == 'create':
#             validated = self._validate('data', body['data'], req, self._data_schema)
#             self.create(r, req, resp, validated, **kwargs)
#
#         elif method == 'query':
#             validated = self._validate('data', body['data'], req, self._query_schema)
#             self.query(r, req, resp, validated, **kwargs)
