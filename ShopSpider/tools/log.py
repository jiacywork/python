# -*- coding: utf-8 -*-

import logging
import os
import time
import datetime


class Logger(logging.Formatter):
    """日志配置"""

    current_path = os.path.dirname(os.path.dirname(__file__))

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=current_path + '/ShopSpiderlog.log',
        filemode='a'
    )

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = str(datetime.datetime.now())
        return s

    def get_logger(self):
        return logging

    def info(self, msg):
        logging.info(msg=msg)

    def error(self, msg):
        logging.error(msg=msg)

    def warn(self, msg):
        logging.warn(msg=msg)
