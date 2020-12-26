# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from ShopSpider.tools.log import Logger


class TaskScheduler:
    """任务调度中心"""

    def __init__(self):
        """初始化任务调度中心"""
        self.scheduler = BlockingScheduler({
            'apscheduler.executors.default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': '20'
            },
            'apscheduler.executors.processpool': {
                'type': 'processpool',
                'max_workers': '5'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '3',
            'apscheduler.timezone': 'Asia/Shanghai',
        })
        self.logger = Logger()
        self.scheduler._logger = self.logger.get_logger()

    def add_job(self, job_id, func, date, **args):
        """添加job"""
        self.logger.info(f"添加job - {job_id}")
        self.scheduler.add_job(id=job_id, func=func, args=args, trigger='date', run_date=date)

    def remove_job(self, job_id):
        """移除job"""
        self.scheduler.remove_job(job_id)
        self.logger.info(f"移除job - {job_id}")

    def pause_job(self, job_id):
        """停止job"""
        self.scheduler.pause_job(job_id)
        self.logger.info(f"停止job - {job_id}")

    def resume_job(self, job_id):
        """恢复job"""
        self.scheduler.resume_job(job_id)
        self.logger.info(f"恢复job - {job_id}")

    def get_jobs(self):
        """获取所有job信息,包括已停止的"""
        res = self.scheduler.get_jobs()
        self.logger.info(f"所有job - {res}")

    def print_jobs(self):
        self.logger.info(f"输出详细job信息")
        self.scheduler.print_jobs()

    def start(self):
        """启动调度器"""
        self.logger.info(f"启动调度器")
        self.scheduler.start()

    def shutdown(self):
        """关闭调度器"""
        self.logger.info(f"关闭调度器")
        self.scheduler.shutdown()
