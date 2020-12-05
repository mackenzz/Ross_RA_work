# -*- coding:utf-8 -*-
import logging
from logging import handlers

logger = logging.getLogger(__name__)

fmt = logging.Formatter(
    '[%(asctime)s %(levelname)-7s %(name)s:%(lineno)d %(message)s')

lvl = logging.INFO

hdl = logging.StreamHandler()
hdl.setLevel(lvl)
hdl.setFormatter(fmt)

file_hdl = handlers.RotatingFileHandler("./log.txt")
file_hdl.setLevel(lvl)
file_hdl.setFormatter(fmt)

logger.handlers.clear()
logger.addHandler(hdl)
logger.addHandler(file_hdl)

logger.setLevel(lvl)
