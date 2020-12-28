# -*- coding: utf-8 -*-

from ShopSpider.spiders.taobao import TaoBao
from ShopSpider import settings
from ShopSpider.scheduler.taskScheduler import TaskScheduler
import uuid
import datetime


if __name__ == '__main__':
    """测试"""
    tb = TaoBao(settings.TB_USERNAME, settings.TB_PASSWORD)
    # 获取当天日期
    now = datetime.datetime.now()
    current_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' '

    scheduler = TaskScheduler()
    # 添加定时登录任务
    scheduler.add_job('taobao-login-' + str(uuid.uuid4()), tb.login, current_date + '19:58:00')
    # 添加定时提交任务
    scheduler.add_job('taobao-submit-' + str(uuid.uuid4()), tb.submit, current_date + '20:00:00')
    scheduler.start()
