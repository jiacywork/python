# -*- coding: utf-8 -*-

from ShopSpider.spiders.taobao import TaoBao
from ShopSpider import settings
from ShopSpider.scheduler.taskScheduler import TaskScheduler
import uuid


if __name__ == '__main__':
    scheduler = TaskScheduler()
    tb = TaoBao(settings.TB_USERNAME, settings.TB_PASSWORD)
    # 添加定时登录任务
    scheduler.add_job('taobao-login-' + str(uuid.uuid4()), tb.login, '2020-12-25 19:58:00')
    # 添加定时提交任务
    scheduler.add_job('taobao-submit-' + str(uuid.uuid4()), tb.submit, '2020-12-25 20:00:00')
    scheduler.start()
