import yaml
import os

from logging.config import dictConfig

CONFIG = {}

for k, v in os.environ.items():
    if k.startswith("TRIPBASE_"):
        name = k[9:]
        CONFIG[name.lower()] = os.environ[k]

def get_logging_config(sentry_url):
    return {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'console': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s '
                          '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                'datefmt': '%H:%M:%S',
                },
            },

        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console'
                },
            'sentry': {
                'level': 'WARNING',
                'class': 'raven.handlers.logging.SentryHandler',
                'dsn': sentry_url,
                },
            },

        'loggers': {
            '': {
                'handlers': ['console', 'sentry'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

# HACK: Little hack to get raven to work with logger
dictConfig(get_logging_config(CONFIG['sentry_url']))


def get_config():
    return CONFIG
