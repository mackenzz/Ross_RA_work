# -*- coding:utf-8 -*-
import pymysql
from conf import config


def db():
    db_config = getattr(config, "DB")
    default = db_config.get("default")
    if default['ENGINE'] == 'pymysql':
        conn = pymysql.connect(host=default['HOST'], port=default['PORT'], db=default['DB_NAME'], user=default['USER'],
                               passwd=default['PASSWORD'])
        sql = conn.cursor(pymysql.cursors.DictCursor)
        return conn, sql


conn, sql = db()
