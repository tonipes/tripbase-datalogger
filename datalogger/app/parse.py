import logging

from .core import field

_logger = logging.getLogger(__name__)


def parse_models(models):
    res = {}
    for model_k, model_v in models.items():

        model = {
            'name': model_v['name'],
            'fields': []
        }

        for field_k, field_v in model_v['fields'].items():
            model['fields'].append(field.get_field(field_v))

        res[model_k] = model

    return res
