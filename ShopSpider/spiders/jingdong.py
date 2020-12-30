# -*- coding: utf-8 -*-

from selenium import webdriver
from ShopSpider.tools.log import Logger
from ShopSpider import settings
import pickle
import time
import datetime
import random
import os


class JingDong:
    """京东爬虫"""

    # 登录网址和主页
    login_url = 'https://passport.jd.com/new/login.aspx'
    domain = "https://www.jd.com/"

    # cookie地址
    current_path = os.path.dirname(__file__)
    cookie = current_path + "/jingdong-cookies.json"

    def __init__(self, username, password):
        """初始化"""
        self.username = username
        self.password = password
        self.logger = Logger()

        self.logger.info("开始初始化浏览器")
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(
            executable_path="/Users/jiachengyu/Downloads/spider_boc/scrapy_spider/chromdriver2.33/chromedriver",
            options=option)
        # 在获取不可用的元素之前，会隐式等待10秒中的时间
        self.browser.implicitly_wait(10)

    def login(self):
        """
        模拟登录京东
        """
        self.logger.info("开始登录京东")
        if os.path.exists(self.cookie):
            self.read_cookie()
        else:
            # 打开主页，并跳转到登录页面
            self.browser.get(self.login_url)
            time.sleep(random.randint(3, 5))
            self.input()

    def re_login(self):
        """
        重新登录
        """
        self.logger.info("cookie已失效，需重新登录")
        # 删除已失效的cookie文件，并重新登录
        if os.path.exists(self.cookie):
            os.remove(self.cookie)
        self.input()

    def input(self):
        """
        键入用户信息并登录
        """
        self.logger.info("选择账户登录方式")
        self.browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[3]/a').click()
        time.sleep(random.randint(1, 2))
        username_el = self.browser.find_element_by_id('loginname')
        username_el.click()
        time.sleep(random.randint(1, 2))
        # 输入登录账号
        self.logger.info("模拟输入用户信息")
        for character in self.username:
            username_el.send_keys(character)
            time.sleep(0.3)
        # 输入登录密码
        pwd_el = self.browser.find_element_by_id('nloginpwd')
        pwd_el.click()
        time.sleep(random.randint(1, 2))
        self.logger.info("模拟输入密码信息")
        for character in self.password:
            pwd_el.send_keys(character)
            time.sleep(0.3)
        # 模拟登录操作
        time.sleep(random.randint(1, 3))
        self.logger.info("模拟登录")
        self.browser.find_element_by_id('loginsubmit').click()
        time.sleep(random.randint(1, 3))
        self.verify()

    def verify(self):
        """
        登录验证
        """
        if self.domain in self.browser.current_url:
            self.logger.info("登录成功")
            self.save_cookie()
        else:
            self.logger.warn("登录后进入未知页面：" + self.browser.current_url)
            pass

    def read_cookie(self):
        """
        读取cookie缓存信息
        """
        self.logger.info("读取已缓存cookie信息")
        self.browser.get(self.login_url)
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

    def quit(self):
        """
        退出浏览器
        """
        self.logger.info("正在退出浏览器")
        self.browser.quit()

    def buy(self, item_url, count):
        """
        进入商品详情页面
        """
        self.browser.get(item_url)
        time.sleep(random.randint(1, 3))
        if self.login_url in self.browser.current_url:
            self.re_login()
            self.buy(item_url=item_url, count=count)
        elif item_url in self.browser.current_url:
            self.logger.info("已进入商品详情页面")
            self.logger.info("开始处理商品数量")
            good_cnt = 1
            while good_cnt < count:
                self.browser.find_element_by_class_name('btn-add').click()
                good_cnt += 1
                time.sleep(0.3)
            self.logger.info("等待到点抢购")
            while True:
                # 由于网络延迟，提前3毫秒执行(具体提前时间可通过ping测试获取)
                if '09:59:59.700' in str(datetime.datetime.now()):
                    self.logger.info("开始抢购")
                    self.browser.find_element_by_id('InitCartUrl').click()
                    # if 'buy.taobao.com' in self.browser.current_url or 'buy.tmall.com' in self.browser.current_url:
                    #     self.logger.info("商品已结算，开始进行订单提交")
                    #     self.browser.find_element_by_id('InitCartUrl').click()
                    #     if 'cashierstl.alipay.com' in self.browser.current_url:
                    #         self.logger.info("已进入支付界面, 订单提交成功")
                    #     else:
                    #         self.logger.info("订单提交失败")
                    # else:
                    #     self.logger.warn("商品结算时进入未知页面：" + self.browser.current_url)
                    break
                elif '09:59:55.000' in str(datetime.datetime.now()):
                    self.logger.info("抢购开始前刷新页面")
                    self.browser.refresh()
                else:
                    time.sleep(0.000001)
            self.logger.info("即将退出浏览器")
            time.sleep(random.randint(15, 30))
            self.quit()
        else:
            self.logger.info("未知页面，当前网页地址:" + self.browser.current_url)


if __name__ == '__main__':
    """定制执行抢购功能"""
    try:
        # 循环等待，抢购前2分钟登录
        while True:
            if '09:58:00' in str(datetime.datetime.now()):
                break
            else:
                time.sleep(0.5)
        # 开始执行抢购程序
        jd = JingDong(username=settings.JD_USERNAME, password=settings.JD_PASSWORD)
        jd.login()
        jd.buy(item_url="https://item.jd.com/100012043978.html", count=2)
    except Exception as e:
        print("功能异常: " + str(e))
        jd.quit()
