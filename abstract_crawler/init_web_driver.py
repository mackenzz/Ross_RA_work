# from selenium.webdriver import Chrome
#
# webdriver_obj = Chrome()




# -*- coding:utf-8 -*-
from selenium import webdriver
import requests


def initdriver():
    # proxy_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=0&city=0&yys=0&port=1&pack=61339&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
    # proxy = requests.get(proxy_url).text
    # print(proxy)
    # proxy = "127.0.0.1:" + str(port)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.add_argument("--proxy-server=http://%s" % proxy)
    # chrome_options.add_argument("--proxy-server=http://%s" % proxy)
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    prefs = {
        'profile.default_content_setting_values': {
            # 'images': 2,  # 不显示图片
            'notifications': 2  # 不显示通知
        },
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False}
    chrome_options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/mackenziezhang/PycharmProjects/untitled/chromedriver") # chromedriver_path
