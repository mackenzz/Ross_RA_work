# -*- coding:utf-8 -*-
from cache import rds


class MarkLinesRedis(object):

    def __init__(self, type):
        self.type = type

    def rpush_info(self, port, values):
        return rds.rpush("mkl_{}:{}".format(self.type, port), values)

    def lpop_info(self, port):
        return rds.lpop("mkl_{}:{}".format(self.type, port))

    def ltrim_info(self, port):
        return rds.ltrim("mkl_{}:{}".format(self.type, port), 1, 0)

    def llen_info(self, port):
        return rds.llen("mkl_{}:{}".format(self.type, port))
