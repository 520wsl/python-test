#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/20'
# 我不懂什么叫年少轻狂，只知道胜者为王
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import time

import moment
import redis
from public.ConfigParser import ConfigParser
from public.Logger import Logger


class Publish():
    def __init__(self):
        self.rds = self.getRds()
        self.logger = self.getLooger()
        pass

    def getRds(self):
        con = ConfigParser()
        pool = redis.ConnectionPool(host=con.getConfig('redisDev', 'host'),
                                    port=con.getConfig('redisDev', 'port'),
                                    db=con.getConfig('redisDev', 'db'))
        return redis.StrictRedis(connection_pool=pool)

    def getLooger(self):
        timeStr = moment.now().format('YYYY-MM-DD-HH-mm-ss')
        logName = 'publish_%s.txt' % (timeStr)
        return Logger(logname=logName, loglevel=1, logger="getBookTXT").getlog()

    def init(self):
        directive = input("publish: >>")
        self.rds.publish('initBook', directive)


if __name__ == '__main__':
    publish = Publish()
    while True:
        directive = input("publish: >>")

        if directive == "init":
            publish.logger.debug("初始化数据")
            time.sleep(30)
            publish.init()

        if directive == "stop":
            publish.logger.debug("停止发布")
            break
        if directive == "catalog":
            publish.logger.debug("发布抓取通知")
            time.sleep(30)
            publish.rds.publish('getBookCatalog', directive)
        if directive == "txt":
            publish.logger.debug("发布抓取通知")
            time.sleep(30)
            publish.rds.publish('getBookTxt', directive)
