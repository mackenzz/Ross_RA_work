# -*- coding: utf-8 -*-


from spiders import BaseScripts
from tools.init_webdriver import initdriver


class MarklinesBaseScripts(BaseScripts):

    def __init__(self, proxy=None):
        super(MarklinesBaseScripts, self).__init__()
        self.driver = None
        self.proxy = proxy

    # 自动登录marklines
    def auto_login(self, port, account, pwd, email):
        self.driver = initdriver(port, proxy=self.proxy)
        url = 'https://www.marklines.com/cn/members/login'
        self.get_to_page(url, 20)

        self.login_first_page(account, pwd)

        self.login_second_page(account, email)

        self.login_first_page(account, pwd)

        print("自动登录完成")

    def login_first_page(self, account, pwd):
        self.wait_xpath_appear("//input[@type='text']", 30)
        self.driver.find_element_by_xpath("//input[@type='text']").click()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(account)

        self.wait_xpath_appear("//input[@type='password']", 10)
        self.driver.find_element_by_xpath("//input[@type='password']").click()
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(pwd)

        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

    def login_second_page(self, account, email):  # 登录要验证邮箱的页面
        self.wait_xpath_appear('//div[@id="form_help_and_guide_pc_memberId"]/input[@type="text"]', 10)
        self.driver.find_element_by_xpath('//div[@id="form_help_and_guide_pc_memberId"]/input[@type="text"]').click()
        self.driver.find_element_by_xpath('//div[@id="form_help_and_guide_pc_memberId"]/input[@type="text"]').send_keys(
            account)

        self.wait_xpath_appear('//div[@id="form_help_and_guide_pc_mailAddress"]/input[@type="text"]', 10)
        self.driver.find_element_by_xpath('//div[@id="form_help_and_guide_pc_mailAddress"]/input[@type="text"]').click()
        self.driver.find_element_by_xpath(
            '//div[@id="form_help_and_guide_pc_mailAddress"]/input[@type="text"]').send_keys(
            email)

        self.driver.find_element_by_xpath('//div[@class="text-center row"]//button[@type="submit"]').click()
