# -*- coding: utf-8 -*-

from selenium import webdriver
from ShopSpider.tools.log import Logger
from ShopSpider import settings
import pickle
import time
import datetime
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

    def start(self):
        """
        模拟登录淘宝网
        """
        self.logger.info("开始登录淘宝网")
        if os.path.exists(self.cookie):
            self.read_cookie()
            self.cart_list()
        else:
            # 打开淘宝网主页，并跳转到登录页面
            self.browser.get(self.domain)
            time.sleep(random.randint(3, 5))
            self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
            time.sleep(random.randint(3, 5))
            self.input()

    def input(self):
        """
        键入用户信息并登录
        """
        username_el = self.browser.find_element_by_xpath('//*[@id="fm-login-id"]')
        username_el.click()
        time.sleep(random.randint(1, 2))
        # 输入淘宝登录账号
        self.logger.info("模拟输入用户信息")
        for character in self.username:
            username_el.send_keys(character)
            time.sleep(0.3)
        # 输入淘宝登录密码
        pwd_el = self.browser.find_element_by_xpath('//*[@id="fm-login-password"]')
        pwd_el.click()
        time.sleep(random.randint(1, 2))
        self.logger.info("模拟输入密码信息")
        for character in self.password:
            pwd_el.send_keys(character)
            time.sleep(0.3)
        # 模拟登录操作
        time.sleep(random.randint(1, 3))
        self.logger.info("模拟登录")
        self.browser.find_element_by_class_name('fm-submit').click()
        time.sleep(random.randint(1, 3))
        self.verify()

    def read_cookie(self):
        """
        读取cookie缓存信息
        """
        self.logger.info("读取已缓存cookie信息")
        self.browser.get('https://login.taobao.com/')
        cookies = pickle.load(open(self.cookie, "rb"))
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        time.sleep(random.randint(3, 5))
        self.browser.get(self.domain)

    def save_cookie(self):
        """
        缓存cookie信息
        """
        self.logger.info("缓存已登录cookie信息")
        pickle.dump(self.browser.get_cookies(), open(self.cookie, "wb"))

    def verify(self):
        """
        登录验证
        """
        if "身份验证" in self.browser.title:
            self.logger.info("需进行登录身份验证")
            # 发送验证码
            # self.browser.find_element_by_xpath('//*[@id="J_GetCode"]').click()
            # time.sleep(random.randint(5, 10))

            # 输入验证码
            # verify_code = self.browser.find_element_by_xpath('//*[@id="J_Phone_Checkcode"]')
            # verify_code.click()
            # time.sleep(random.randint(1, 3))
            # for character in "":
            #     verify_code.send_keys(character)
            #     time.sleep(0.3)

            # 模拟确定按钮
            # self.browser.find_element_by_xpath('//*[@id="submitBtn"]').click()
            time.sleep(random.randint(3, 5))
        elif 'www.taobao.com' in self.browser.current_url:
            self.logger.info("登录成功")
            self.save_cookie()
            self.cart_list()
        else:
            self.logger.warn("登录后进入未知页面：" + self.browser.current_url)
            pass

    def cart_list(self):
        """
        进入购物车页面
        """
        time.sleep(random.randint(3, 5))
        # 判断是否为购物车界面(可能存在cookie失效的情况，打开的是登录页面)
        if 'login.taobao.com' in self.browser.current_url:
            self.re_login()
        elif 'cart.taobao.com' in self.browser.current_url:
            self.select_all()
        elif 'www.taobao.com' in self.browser.current_url:
            self.details()
        else:
            self.logger.info("未知页面，当前网页地址:" + self.browser.current_url)
            pass

    def re_login(self):
        """
        重新登录
        """
        self.logger.info("cookie已失效，需重新登录")
        # 删除已失效的cookie文件，并重新登录
        if os.path.exists(self.cookie):
            os.remove(self.cookie)
        self.input()

    def details(self):
        """
        查看购物车详情
        """
        self.logger.info("即将进入购物车页面")
        self.browser.find_element_by_xpath('//*[@id="mc-menu-hd"]').click()
        time.sleep(random.randint(3, 5))
        self.cart_list()

    def select_all(self):
        """
        全选购物车商品
        """
        self.logger.info("已成功进入购物车界面")
        all_btn = self.browser.find_element_by_xpath('//*[@id="J_SelectAll1"]')
        if "select-all-disabled" in all_btn.get_attribute("class"):
            self.logger.info("购物车内商品已全部失效...")
            pass
        else:
            self.logger.info("全选购物车内商品")
            all_btn.click()
            self.submit()
   
    def submit(self):
        """
        点击提交订单
        """
        self.logger.info("即将进行商品结算")
        settle_btn = self.browser.find_element_by_xpath('//*[@id="J_SmallSubmit"]')
        while True:
            # 由于网络延迟，提前3毫秒执行(具体提前时间可通过ping测试获取)
            if '19:59:59.900' in str(datetime.datetime.now()):
                settle_btn.click()
                if 'buy.taobao.com' in self.browser.current_url or 'buy.tmall.com' in self.browser.current_url:
                    self.logger.info("商品已结算，开始进行订单提交")
                    self.browser.find_element_by_class_name('go-btn').click()
                    if 'cashierstl.alipay.com' in self.browser.current_url:
                        self.logger.info("已进入支付界面, 订单提交成功")
                        pass
                    else:
                        self.logger.info("订单提交失败")
                        pass
                else:
                    self.logger.warn("商品结算时进入未知页面：" + self.browser.current_url)
                    pass
                break
            else:
                time.sleep(0.000001)
        self.logger.info("即将退出浏览器")
        time.sleep(random.randint(15, 30))
        self.quit()

    def quit(self):
        """
        退出浏览器
        """
        self.logger.info("正在退出浏览器")
        self.browser.quit()


if __name__ == '__main__':
    """定制执行淘宝抢购功能"""
    try:
        # 循环等待，抢购前2分钟登录淘宝
        while True:
            if '19:58:00' in str(datetime.datetime.now()):
                break
            else:
                time.sleep(0.5)
        # 开始执行抢购程序
        tb = TaoBao(username=settings.TB_USERNAME, password=settings.TB_PASSWORD)
        tb.start()
    except Exception as e:
        print("功能异常: " + str(e))
        tb.quit()
