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
from getText.getTest12.getTest15 import SaveBookToRedis
from public.ConfigParser import ConfigParser
from public.DataToo import DataToo
from public.Logger import Logger
from public.MySqlToo import MySqlToo
from public.RedisToo import RedisToo
from public.TimeToo import TimeToo

pool = redis.ConnectionPool(host='192.168.2.202',
                            port=6379, db=8)
r = redis.StrictRedis(connection_pool=pool)
p = r.pubsub()
p.subscribe("initBook", "cctv1")
for item in p.listen():
    print("Listen on channel : %s " % item['channel'].decode())
    if item['type'] == 'message':
        data = item['data'].decode()
        print("From %s get message : %s" % (item['channel'].decode(), item['data'].decode()))
        second = 1
        environmentalType = 1
        maxBookNex = 0
        bookPageSize = 10
        bookIdSize = 5

        timeStr = moment.now().format('YYYY-MM-DD-HH-mm-ss')
        logName = 'getBookTXT_%s.txt' % (timeStr)


        logger = Logger(logname=logName, loglevel=1, logger="getBookTXT").getlog()

        if environmentalType == 2:
            environmental = 'online'
            getBookIdsSql = "SELECT book_Id FROM books WHERE nex > %s" % maxBookNex
        elif environmentalType == 1:
            environmental = 'test'
            testBookId = '0,1000'
            getBookIdsSql = "SELECT book_Id FROM books WHERE nex > %s limit %s" % (maxBookNex, testBookId)
        else:
            environmental = 'dev'
            testBookId = "'10000611804961003','10000828104982003'"
            getBookIdsSql = "SELECT book_Id FROM books WHERE book_Id in (%s)" % testBookId

        mysqlStr = {
            'saveText': "INSERT INTO `links` (`url`,article) VALUES (%s, %s) ON DUPLICATE KEY UPDATE article = VALUES (article), nex = nex+1",
            'getBookIdsSql': getBookIdsSql,
            'getCatalogData': "SELECT url FROM links WHERE fs = 0 AND book_Id in "
        }

        bookTxt = SaveBookToRedis(mysqlStr=mysqlStr, bookPageSize=bookPageSize, bookIdSize=bookIdSize)
        bookTxt.control()
        logger.debug('redis 储存成功')
        if item['data'] == 'over1':
            print(item['channel'].decode(), '停止发布')
            break
p.unsubscribe('spub')
