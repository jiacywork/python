# -*- coding: utf-8 -*-

import logging
import os
from ShopSpider.tools.LoggingFormat import MyFormatter


class Logger():
    """日志配置"""

    current_path = os.path.dirname(os.path.dirname(__file__))

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.current_path + '/ShopSpiderlog.log',
            filemode='a'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        self.logger.addHandler(console)

        formatter = MyFormatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d,%H:%M:%S.%f')
        console.setFormatter(formatter)

    def get_logger(self):
        return self.logger

    def info(self, msg):
        self.logger.info(msg=msg)

    def error(self, msg):
        self.logger.error(msg=msg)

    def warn(self, msg):
        self.logger.warning(msg=msg)


if __name__ == '__main__':
    logger = Logger()
    logger.info("test")
