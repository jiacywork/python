# -*- coding: utf-8 -*-

from selenium import webdriver
from ShopSpider.tools.log import Logger
import pickle
import time
import random
import os


class TaoBao:
    """
    淘宝网爬虫
    """

    domain = "https://www.taobao.com/"

    current_path = os.path.dirname(__file__)
    cookie = current_path + "/taobao-cookies.json"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logger = Logger()

        self.logger.info("开始初始化浏览器")
        option = webdriver.ChromeOptions()
        # 这里去掉window.navigator.webdriver的特性
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 下面的chromedriver.exe使用特殊的可执行文件，去掉了$cdc_lasutopfhvcZLmcfl等特性
        self.browser = webdriver.Chrome(
            executable_path="/Users/jiachengyu/Downloads/spider_boc/scrapy_spider/chromdriver2.33/chromedriver",
            options=option)
        # 在获取不可用的元素之前，会隐式等待10秒中的时间
        self.browser.implicitly_wait(10)

    def login(self):
        """
        模拟登录淘宝网
        """
        self.logger.info("开始登录淘宝网")
        if os.path.exists(self.cookie):
            self.read_cookie()
            self.good_details()
        else:
            # 打开淘宝网主页，并跳转到登录页面
            self.browser.get(self.domain)
            time.sleep(random.randint(1, 3))
            self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
            time.sleep(random.randint(1, 3))
            self.input()

    def input(self):
        """
        键入用户信息并登录
        """
        username_el = self.browser.find_element_by_xpath('//*[@id="fm-login-id"]')
        username_el.click()
        time.sleep(random.randint(1, 3))
        # 输入淘宝登录账号
        for character in self.username:
            username_el.send_keys(character)
            time.sleep(0.3)
        # 输入淘宝登录密码
        pwd_el = self.browser.find_element_by_xpath('//*[@id="fm-login-password"]')
        pwd_el.click()
        time.sleep(random.randint(1, 3))
        for character in self.password:
            pwd_el.send_keys(character)
            time.sleep(0.3)
        # 模拟登录操作
        time.sleep(random.randint(1, 3))
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
        time.sleep(random.randint(3, 5))

        # 判断是否需要进行身份校验
        if "身份验证" in self.browser.title:
            self.verify()
        self.save_cookie()
        self.good_details()

    def read_cookie(self):
        """
        读取cookie缓存信息
        """
        self.logger.info("读取已缓存cookie信息")
        self.browser.get(self.domain)
        cookies = pickle.load(open(self.cookie, "rb"))
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        self.browser.get(self.domain)

    def save_cookie(self):
        """
        缓存cookie信息
        """
        pickle.dump(self.browser.get_cookies(), open(self.cookie, "wb"))

    def verify(self):
        """
        身份验证
        """
        self.logger.ingo("登录身份验证")
        # 发送验证码
        self.browser.find_element_by_xpath('//*[@id="J_GetCode"]').click()
        time.sleep(random.randint(5, 10))

        # 输入验证码
        # verify_code = browser.find_element_by_xpath('//*[@id="J_Phone_Checkcode"]')
        # verify_code.click()
        # time.sleep(random.randint(1, 3))
        # for character in "":
        #     verify_code.send_keys(character)
        #     time.sleep(0.3)

        # 模拟确定按钮
        self.browser.find_element_by_xpath('//*[@id="submitBtn"]').click()
        time.sleep(random.randint(3, 5))

    def good_details(self):
        """
        进入购物车页面，并全选商品
        """
        # 点击购物车
        self.logger.info("进入购物车页面")
        self.browser.find_element_by_xpath('//*[@id="mc-menu-hd"]').click()
        time.sleep(random.randint(3, 5))

        # 判断是否为购物车界面(可能存在cookie失效的情况，打开的是登录页面)
        if 'login.taobao.com' in self.browser.current_url:
            self.logger.ingo("cookie已失效，需重新登录")
            self.input()
        else:
            # 全选商品
            all_btn = self.browser.find_element_by_xpath('//*[@id="J_SelectAll1"]')
            if "select-all-disabled" in all_btn.get_attribute("class"):
                self.logger.ingo("购物车内商品已全部失效...")
                pass
            else:
                self.logger.info("全选购物车内商品")
                all_btn.click()

    def submit(self):
        """
        点击提交订单
        """
        # 模拟点击结算按钮
        self.logger.info("开始进行商品结算")
        self.browser.find_element_by_xpath('//*[@id="J_SmallSubmit"]').click()
        # 模拟提交订单按钮
        self.logger.info("开始进行订单提交")
        self.browser.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div[1]/a[2]').click()
        time.sleep(random.randint(5, 10))
        self.quit()

    def quit(self):
        """
        退出浏览器
        """
        self.logger.info("退出浏览器")
        self.browser.quit()


# if __name__ == '__main__':
#     try:
#         tb = TaoBao(settings.TB_USERNAME, settings.TB_PASSWORD)
#         tb.login()
#         scheduler = BlockingScheduler()
#         scheduler.add_job(tb.submit, 'cron', day_of_week='0-6', hour=21, minute=50, second=30)
#         scheduler.start()
#     except Exception as e:
#         log.error("功能异常: " + e)
#         tb.quit()
