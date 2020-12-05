# -*- coding:utf-8 -*-
import redis
from conf import config


def cache():
    db_config = getattr(config, "CACHE")
    default = db_config.get("default")
    if default['ENGINE'] == 'redis':
        rds = redis.StrictRedis(host=default['HOST'], password=default.get('PASSWORD'), port=default['PORT'],
                                db=default['DB'])
        return rds


rds = cache()
