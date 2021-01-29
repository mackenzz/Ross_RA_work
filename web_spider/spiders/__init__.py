# -*- coding:utf-8 -*-
from functools import wraps
import traceback

from selenium.webdriver.common.by import By  # 设置EC判断通过 BY 什么什么（eg:XPATH）来查找
from selenium.webdriver.support.ui import WebDriverWait  # 设置访问超时时间，直到某某条件达成
from selenium.webdriver.support import expected_conditions as EC  # EC判断，来自动等待,原理是每500毫秒去检测一次

from selenium.common.exceptions import TimeoutException

from tools.log import logger


class BaseScripts(object):

    def __init__(self):
        self.driver = None

    # 打开页面，并设置时间(单位秒)，超时返回1
    def get_to_page(self, url, time):
        self.driver.implicitly_wait(time)
        self.driver.set_page_load_timeout(time)
        try:
            self.driver.get(url)
        except TimeoutException:
            logger.error("打开" + url + "页面%d秒超时，请更换代理重试" % time)
            return "1"

    def wait_xpath_appear(self, xpath, time):
        try:
            WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logger.error("等待Xpath:" + xpath + "%d秒超时" % time)
            return "1"

    def scroll_down(self):
        js = "window.scrollBy(0, 10000);"
        try:
            self.driver.execute_script(js)
        except TimeoutException:
            pass


def error_tracker(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            rs = fn(*args, **kwargs)
        except Exception as e:
            logger.fatal(f"系统错误:{traceback.format_exc()}")
            raise Exception(e)
        return rs

    return decorated
