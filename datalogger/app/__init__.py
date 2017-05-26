import logging

import falcon
import redis
import raven
import os
from raven import Client
from raven.middleware import Sentry

from .core import engine, middleware
from . import config
from . import resource
from . import sink

conf = config.get_config()

_logger = logging.getLogger(__name__)

pool = redis.ConnectionPool(
    host=conf['redis_url'],
    port=conf['redis_port'],
    db=conf['redis_db']
)

master_key = conf['master_key']
redis_engine = engine.RedisEngine(pool)

app = falcon.API(middleware=[
    middleware.RequestContextMiddleware(redis_engine),
    middleware.AuthMiddleware(redis_engine, [master_key]),
    middleware.JsonRequestMiddleware(redis_engine),
    middleware.JsonResponseMiddleware(redis_engine),
])

sink = sink.Sink()
app.add_sink(sink.get_sink, '/')

log_res = resource.LocationLogResource(redis_engine)
app.add_route('/log/', log_res)

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
