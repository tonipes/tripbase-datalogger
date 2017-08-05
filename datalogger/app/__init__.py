import logging

import falcon
import yaml
import redis
import raven
import os
from raven import Client
from raven.middleware import Sentry

from .core import engine, middleware, resource
from . import config
from . import sink
from . import parse

conf = config.get_config()

_logger = logging.getLogger(__name__)

models = []

with open(conf['model_definition'], 'r') as stream:
    d = yaml.load(stream)
    print(d)
    models = parse.parse_models(d)

print(models)

pool = redis.ConnectionPool(
    host=conf['redis_url'],
    port=conf['redis_port'],
    db=conf['redis_db']
)

master_key = conf['master_key']
redis_engine = engine.RedisEngine(pool, models)

app = falcon.API(middleware=[
    middleware.RequestContextMiddleware(redis_engine),
    middleware.AuthMiddleware(redis_engine, [master_key]),
    middleware.JsonRequestMiddleware(redis_engine),
    middleware.JsonResponseMiddleware(redis_engine),
])

sink = sink.Sink()
app.add_sink(sink.get_sink, '/')

model_res = resource.ModelResource(redis_engine)
app.add_route('/api/{model}', model_res)

raven_client = Client(
    conf['sentry_url'],
    # release=raven.fetch_git_sha(os.getcwd()),
    include_paths=[__name__.split('.', 1)[0]],
    environment=conf['environment'],
    processors=(
        'raven.processors.SanitizePasswordsProcessor',
    ),
)

_logger.debug("Starting up server")
app = Sentry(app, raven_client)
