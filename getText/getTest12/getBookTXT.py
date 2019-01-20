#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '文章抓取'
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
import math
import random
import threading
import moment
import time

from lxml import etree

from public.MySqlToo import MySqlToo
from public.Logger import Logger
from public.DataToo import DataToo
from public.ConfigParser import ConfigParser
from public.TimeToo import TimeToo


class BookTXTLoad(object):
    def __init__(self, bookPageSize, webConfig, bookIdSize, second,
                 bookTXTGroupSize, mysqlStr):
        self.b_bookPageSize = bookPageSize
        self.b_bookIdSize = bookIdSize
        self.b_bookTXTGroupSize = bookTXTGroupSize
        self.b_second = second
        self.b_host = webConfig['host']
        self.b_heads = webConfig['heads']
        self.b_mysqlStr = mysqlStr
        self.b_catalogList = []
        self.b_bookTXTData = []
        self.errorUrl = []
        self.request404 = []
        self.countNum = 0
        self.countMsg = {
            'title': webConfig['title'],
            'time': webConfig['time'],
            'author': webConfig['author'],
            'email': webConfig['email'],
            'bookSize': 0,
            'bookGroupSize': 0,
            'bookTaskSize': 0
        }

    def second(self):
        time.sleep(self.b_second)

    # 2、调用mySQL类 mysqlUtils.getListData 获取数据列表
    def getBookData(self):
        bookList = []
        bookData = mySql.getListData(sql=self.b_mysqlStr['getBookIdsSql'])
        for item in bookData:
            bookList.append(item[0])
        return bookList

    def getCatalogData(self, bookId, index):
        catalogList = []
        sql = '%s %s' % (self.b_mysqlStr['getCatalogData'], dataToo.listToStr(bookId))
        logger.info('查询小说章节 [ %s ]...\n' % (sql))
        catalogData = mySql.getListData(sql=sql)
        for item in catalogData:
            catalogList.append(item[0])
        self.b_catalogList.append(catalogList)

    #     4、 章节目录 catalog 数据整理 数组
    def setCatalogList(self, bookGroupingData):
        bookData = bookGroupingData['listTaskList']
        if len(bookData) <= 0:
            logger.debug('setCatalogList 没有数据\n')
            return
        bookIdGroupingData = dataToo.groupingData(list=bookData, pageSize=self.b_bookIdSize)
        listTaskList = bookIdGroupingData['listTaskList']
        for i in range(bookIdGroupingData['listGroupSize']):
            if len(listTaskList[i]) <= 0: continue
            dataToo.threads(listTaskList[i], self.getCatalogData)

    def getArticle(self, link, group, bookCatalogUrlGroupingData, ngroup, nindex):
        bkd = bookCatalogUrlGroupingData
        self.b_heads['Referer'] = link
        logger.info('已采集 [ %s ] 书籍组 [ %s / %s ] 目录组 [ %s / %s ] 文章组 [ %s / %s ] 链接 [ %s ] %s 秒后开始抓取' % (
            self.countNum, group + 1, len(self.b_catalogList), ngroup + 1, bkd['listGroupSize'], nindex + 1,
            bkd['listTaskSize'], link,
            self.b_second))
        self.second()
        text = dataToo.getText(link=link, heads=self.b_heads)
        if len(text['data']) <= 0:
            self.errorUrl.append(link)
            self.countNum += 1
            logger.debug('第 %s 条链接：数据抓取异常 ：%s\n' % (self.countNum, text))
            return
        html = etree.HTML(text['data'])
        content_list = html.xpath('//div[@class="read-content j_readContent"]')
        if len(content_list) <= 0:
            self.countNum += 1
            title = html.xpath('//title/text()')
            requestIntercept = html.xpath('//div[@class="empty-text"]//strong/text()')
            request404 = html.xpath('//h3[@class="lang"]/text()')
            logger.debug('第 %s 条链接：HTML解析异常！' % (self.countNum))
            logger.debug('第 %s 条链接[title]：%s' % (self.countNum, title))
            if len(requestIntercept) > 0:
                self.errorUrl.append(link)
                second = self.b_second * 180
                logger.debug('第 %s 条链接[requestIntercept]：%s 被拦截了暂停 %s 秒后 抓取下一条链接 '
                             % (self.countNum, requestIntercept, second))
                time.sleep(second)
            if len(request404) > 0:
                self.request404.append(link)
                logger.debug('第 %s 条链接[request404]：%s' % (self.countNum, request404))
            logger.debug('第 %s 条链接[text]：%s\n' % (self.countNum, text))
            return
        content_list = content_list[0]
        content = etree.tostring(content_list, method='xml').decode('utf-8')
        res = mySql.batchAdd(sql=self.b_mysqlStr['saveText'], data_info=[(link, content)])
        if res:
            self.errorUrl.append(link)
        self.countNum += 1
        logger.debug('第 %s 条链接： %s\n' % (self.countNum, res))
        # self.b_bookTXTData.append((link, content))

    #     6、循环调用 getBookTxt()

    # 根据章节 catalogId、url 抓取页面数据
    def getBookTXT(self, catalogList, index):
        if len(catalogList) <= 0:
            logger.debug('书籍组 [ %s / %s ] ：getBookTXT 没有数据\n' % (index + 1, len(self.b_catalogList)))
            return
        bookCatalogUrlGroupingData = dataToo.groupingData(list=catalogList, pageSize=self.b_bookTXTGroupSize,
                                                          fixed=True)
        listTaskList = bookCatalogUrlGroupingData['listTaskList']
        for i in range(bookCatalogUrlGroupingData['listGroupSize']):
            if len(listTaskList[i]) <= 0: continue
            # dataToo.threads(listTaskList[i], self.getArticle)
            start = time.time()
            for j in range(len(listTaskList[i])):
                self.second()
                self.getArticle(listTaskList[i][j], index, bookCatalogUrlGroupingData, i, j)
            end = time.time()
            logger.debug('书籍组 [ %s / %s ] 目录组 [ %s / %s ] : 开始时间：%s ： 结束时间：%s ==> 共消耗时间 ：%s 秒 [ %s ]\n' % (
                index + 1, len(self.b_catalogList), i + 1, bookCatalogUrlGroupingData['listGroupSize'],
                float(start), float(end), int(float(end) - float(start)),
                timeToo.changeTime(int(float(end) - float(start)))))

    def saveText(self):
        for i in range(len(self.b_catalogList)):
            if len(self.b_catalogList[i]) <= 0:
                logger.debug('书籍组 [ %s / %s ] saveText 没有数据\n' % (i + 1, len(self.b_catalogList)))
                continue
            start = time.time()
            self.getBookTXT(self.b_catalogList[i], i)
            end = time.time()
            logger.debug('书籍组 [ %s / %s ] : 开始时间：%s ： 结束时间：%s ==> 共消耗时间 ：%s 秒 [ %s ]\n' % (
                i + 1, len(self.b_catalogList), float(start), float(end), int(float(end) - float(start)),
                timeToo.changeTime(int(float(end) - float(start)))))
            logger.info('*-*-*-*-*-*-' * 15)
            # res = mySql.batchAdd(sql=self.b_mysqlStr['saveText'], data_info=self.b_bookTXTData)
            # if res: self.b_bookTXTData = []

    # 文章内容存储
    def bookTxtLoad(self):
        bookData = self.getBookData()
        if len(bookData) <= 0:
            logger.debug('bookTxtLoad 没有数据\n')
            return
        bookGroupingData = dataToo.groupingData(list=bookData, pageSize=self.b_bookPageSize)

        logger.info('========' * 15)
        logger.info("\t时间: %s" % (moment.now().format('YYYY-MM-DD HH:mm:ss')))
        logger.info("\t网站：%s" % (self.b_host))
        logger.info("\t\t\t本次将采集 %s 本小说。\n" % (bookGroupingData['listSize']))
        logger.info('\t\t\t%s 本小说，共分为 %s 个组,每组 %s 本小说。 \n' % (
            bookGroupingData['listSize'], bookGroupingData['listGroupSize'], bookGroupingData['listTaskSize']))
        logger.info('\t\t\t采集时间预算：共 %s 组，每组采集间隔 %s 秒，每组 %s 本小说，每本小说 预计 %s 秒，每组预计 %s 秒，总计 %s 秒 [ %s ]\n' % (
            bookGroupingData['listGroupSize'],
            self.b_second, bookGroupingData['listTaskSize'],
            self.b_second + 10,
            self.b_second + (self.b_second + 10) * bookGroupingData['listTaskSize'],
            (self.b_second + (bookGroupingData['listTaskSize']
                              * (self.b_second + 10))) * bookGroupingData['listGroupSize'],
            timeToo.changeTime(((self.b_second + (bookGroupingData['listTaskSize'] * (self.b_second + 10))))
                               * bookGroupingData['listGroupSize'])))
        logger.info('========' * 15)
        self.setCatalogList(bookGroupingData)
        self.saveText()


if __name__ == '__main__':
    start = time.time()
    con = ConfigParser()
    maxBookNex = 0
    maxCatalogNex = 1
    bookPageSize = 10
    environmentalType = 0
    bookIdSize = 5
    bookTXTGroupSize = 1
    second = 0.5

    timeStr = moment.now().format('YYYY-MM-DD-HH-mm-ss')
    logName = 'getBookTXT_%s.txt' % (timeStr)
    logger = Logger(logname=logName, loglevel=1, logger="getBookTXT").getlog()

    if environmentalType == 2:
        environmental = 'online'
        getBookIdsSql = "SELECT book_Id FROM books WHERE nex > %s" % maxBookNex
    elif environmentalType == 1:
        environmental = 'test'
        testBookId = '0,10000'
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

    webConfig = {
        'host': 'http://www.xs8.cn',
        'title': '小说文章采集',
        'time': timeStr,
        'author': 'Mad Dragon',
        'email': '395548460@qq.com',
        'heads': ''
    }
    heads = {}
    heads['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    heads['Accept-Encoding'] = 'gzip, deflate, br'
    heads['Accept-Language'] = 'zh-CN,zh;q=0.9'
    heads['Connection'] = 'keep-alive'
    heads['Cookie'] = 'newstatisticUUID=1547076169_1527614489; qdrs=0%7C3%7C0%7C0%7C1; qdgd=1'
    heads['Host'] = 'www.xs8.cn'
    heads['Upgrade-Insecure-Requests'] = '1'
    heads['Referer'] = ''
    heads[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    webConfig['heads'] = heads
    timeToo = TimeToo()
    mySql = MySqlToo(logName=logName)
    dataToo = DataToo(logName=logName, second=second)
    book = BookTXTLoad(bookPageSize=bookPageSize, webConfig=webConfig, bookIdSize=bookIdSize, second=second,
                       bookTXTGroupSize=bookTXTGroupSize, mysqlStr=mysqlStr)
    book.bookTxtLoad()
    end = time.time()

    logger.info('---' * 30)
    logger.info('\t\t时间              ：%s' % (moment.now().format('YYYY-MM-DD HH:mm:ss')))
    logger.info('\t\t消耗 时间         ：%s 秒 [ %s ]' % (float(end) - float(start),
                                                    timeToo.changeTime(float(end) - float(start))))
    logger.info('\t\t采集 链接         : %s 条' % (book.countNum))
    logger.info('\t\t采集 失败链接     : %s 条' % (len(book.errorUrl)))
    logger.info('\t\t请求 失败链接     : %s 条' % (len(book.request404)))
    logger.info('\t\t采集 失败链接     ：\n\t\t\t' % (book.errorUrl))
    logger.info('\t\t请求 失败链接     ：\n\t\t\t' % (book.request404))
