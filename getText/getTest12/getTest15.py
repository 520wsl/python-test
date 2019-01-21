#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'redis发布者'
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/12'
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
from public.DataToo import DataToo
from public.MySqlToo import MySqlToo
from public.RedisToo import RedisToo
from public.TimeToo import TimeToo
from public.Logger import Logger


class SaveBookToRedis():
    def __init__(self, mysqlStr, bookPageSize, bookIdSize):
        self.b_mysqlStr = mysqlStr
        self.b_bookPageSize = bookPageSize
        self.b_bookIdSize = bookIdSize

    def getBookData(self):
        bookList = []
        bookData = mySql.getListData(sql=self.b_mysqlStr['getBookIdsSql'])
        for item in bookData:
            bookList.append(item[0])
        return bookList

    def setCatalogList(self, bookGroupingData):
        bookData = bookGroupingData['listTaskList']
        if len(bookData) <= 0:
            logger.debug('setCatalogList 没有数据\n')
            return
        bookIdGroupingData = dataToo.groupingData(list=bookData, pageSize=self.b_bookIdSize)
        listTaskList = bookIdGroupingData['listTaskList']
        for i in range(bookIdGroupingData['listGroupSize']):
            if len(listTaskList[i]) <= 0: continue
            data = []
            for item in listTaskList[i]:
                data.append(str(item))
            r.setListData('bookIdsList', data)

    def control(self):
        bookData = self.getBookData()
        if len(bookData) <= 0:
            logger.debug('bookTxtLoad 没有数据\n')
            return
        bookGroupingData = dataToo.groupingData(list=bookData, pageSize=self.b_bookPageSize)
        self.setCatalogList(bookGroupingData)


if __name__ == '__main__':
    second = 1
    environmentalType = 1
    maxBookNex = 0
    bookPageSize = 10
    bookIdSize = 5

    timeStr = moment.now().format('YYYY-MM-DD-HH-mm-ss')
    logName = 'getBookTXT_%s.txt' % (timeStr)

    start = time.time()
    con = ConfigParser()
    r = RedisToo()
    
    timeToo = TimeToo()
    mySql = MySqlToo(logName=logName)
    dataToo = DataToo(logName=logName, second=second)
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
    # saveBookToRedis.control()
    end = time.time()

    pool = redis.ConnectionPool(host='192.168.2.202',
                                port=6379, db=8)
    r2 = redis.StrictRedis(connection_pool=pool)
    while True:
        msg = input("publish: >>")
        if msg == "stop":
            logger.debug("停止发布")
            break
        if msg == "catalog":
            logger.debug("发布抓取通知")
            saveBookToRedis = SaveBookToRedis(mysqlStr=mysqlStr, bookPageSize=bookPageSize, bookIdSize=bookIdSize)
            saveBookToRedis.control()
            time.sleep(60)
            r2.publish('getBookCatalog', msg)
        if msg == "txt":
            logger.debug("发布抓取通知")
            saveBookToRedis = SaveBookToRedis(mysqlStr=mysqlStr, bookPageSize=bookPageSize, bookIdSize=bookIdSize)
            saveBookToRedis.control()
            time.sleep(60)
            r2.publish('getBookTxt', msg)
