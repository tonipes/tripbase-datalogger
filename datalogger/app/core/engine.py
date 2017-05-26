import redis
import logging
import datetime

from . import search

_logger = logging.getLogger(__name__)

FORMAT_ID_COUNTER = "id_counter:{model_name}"
FORMAT_FIELD_INDEX = "index:{model_name}:{field_name}"

FORMAT_FIELD_KEY = "{model_name}:{id_number}"

FORMAT_FIELD_INDEX_MEMBER = "{field_value}:{id_number}"

class Engine(object):
    pass


class RedisEngine(Engine):
    def __init__(self, pool):
        self.pool = pool

    def _get_id_counter(self, model_name):
        return FORMAT_ID_COUNTER.format(
            model_name=model_name
        )

    def _get_key(self, model_name, id_number):
        return FORMAT_FIELD_KEY.format(
            model_name=model_name,
            id_number=id_number
        )


    def _get_new_id(self, model_name, r):
        # Create if it doesn't exist
        c_field = self._get_id_counter(model_name)
        r.setnx(c_field, 1)
        return r.incr(c_field)

    def _get_field_index_key(self, model_name, field_name):
        return FORMAT_FIELD_INDEX.format(
            model_name=model_name,
            field_name=field_name
        )

    def _get_meta_fields(self):
        return { "_write_time": datetime.datetime.now().timestamp() }

    def get_db(self) -> redis.Redis:
        return redis.Redis(connection_pool=self.pool)

    def query(self, model_name, obj, r):
        _logger.debug("Query at engine: {}".format(obj))

    def create(self, model_name, obj, r):
        _logger.debug("Create at engine: {}".format(obj))
        id_num = self._get_new_id(model_name, r)
        key = self._get_key(model_name, id_num)
        obj.update(self._get_meta_fields())
        r.hmset(key, obj)

        for field_name, field_value in obj.items():
            if field_value is not None:
                if isinstance(field_value, (int, float)): # ZADD score
                    r.zadd(
                        self._get_field_index_key(model_name, field_name),
                        id_num, field_value   # name, score
                    )
                else: # ZADD lex
                    r.zadd(
                        self._get_field_index_key(model_name, field_name),
                        FIELD_INDEX_MEMBER.format(
                            field_value=field_value,
                            id_number=id_num
                        ), 0
                    )
