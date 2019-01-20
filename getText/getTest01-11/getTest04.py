#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/8'
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

import requests
import json
import pymysql
from datetime import datetime, time
from bs4 import BeautifulSoup
from lxml import etree


class load_book(object):
    def __init__(self, host, pageSize):
        self.b_host = host
        self.b_pageSize = pageSize
        self.b_link = self.b_link_load()
        self.b_html_text = self.getHtmlText()
        self.mysql_ip = "172.30.34.210"
        self.mysql_user = "root"
        self.mysql_pwd = "root"
        self.mysql_database = "pythonTest"

    # 链接处理
    def b_link_load(self):
        # https://www.xs8.cn/all?pageSize=10&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=1
        return self.b_host + '/all?pageSize=' + str(
            self.b_pageSize) + '&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=1'

    # 抓取页面元素
    def getHtmlText(self):
        heads = {}
        heads['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        heads['Accept - Encoding'] = 'gzip, deflate, br'
        heads['Accept - Language'] = 'zh-CN,zh;q=0.9'
        heads['Cookie'] = 'newstatisticUUID=1546996330_2089765158; qdrs=0%7C3%7C0%7C0%7C1; qdgd=1'
        heads['Host'] = self.b_host[7:]
        heads[
            'Referer'] = 'https://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=1'
        heads[
            'User - Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        heads['X - Requested - With'] = 'XMLHttpRequest'

        try:
            r = requests.get(self.b_link, headers=heads)
            r.encoding = "utr-8"
            return r.text
        except:
            print("获取列表失败,一秒后重试，失败链接：", self.b_link)
            time.seleep(1)
            self.b_link_load()

    # 解析页面元素
    def parseWithXpath(self):
        html = etree.HTML(self.b_html_text)
        content_list = html.xpath('//div[@class="right-book-list"]//li')
        print(len(content_list))
        content = []
        for item in content_list:
            # 找到所有的 div_h3 标记
            book_Id = item.xpath('.//div[@class="book-info"]/h3/a/@href')[0][6:]
            book_name = item.xpath('.//div[@class="book-info"]/h3/a/text()')[0]
            author = item.xpath('.//div[@class="book-info"]/h4/a/text()')[0]
            tag = item.xpath('.//div[@class="book-info"]/p[@class="tag"]/span/text()')
            synoptic = item.xpath('.//div[@class="book-info"]/p[@class="intro"]/text()')[0]
            img_url = item.xpath('.//div[@class="book-img"]/a/img/@src')[0]
            chan_name = tag[0]
            state = tag[1]
            # print(book_Id)
            # print(book_name)
            # print(tag[1])
            # print(author)
            # print(tag[0])
            # print(synoptic)
            # print(img_url)
            content.append({
                'book_Id': book_Id,
                'book_name': book_name,
                'state': state,
                'author': author,
                'chan_name': chan_name,
                'synoptic': synoptic,
                'img_url': img_url
            })
        # print(content)
        return content

    # 数据库信息
    def openMySqlConfig(self):
        return pymysql.connect(self.mysql_ip, self.mysql_user, self.mysql_pwd, self.mysql_database)

    # 批量添加 信息
    def batchAdd(self, sql, data_info):
        db = self.openMySqlConfig()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        try:
            # 执行sql语句
            cursor.executemany(sql, data_info)
            # 提交到数据库执行
            db.commit()
            db.close()
            return True
        except:
            # 如果发生错误则回滚
            db.rollback()
            db.close()
            return False

    def saveBooks(self, data_info):
        # data_info = [('6972481904230701', '晚安，总裁大人', '连载中', '纳兰雪央', '现代言情', '\r                        【女强爽文，打脸啪啪啪，1V1双洁专宠】\r\n“雷先生，听闻最近有流言说您暗恋我？”\r\n对面男人冷脸头也不抬处理公事。\r\n“我对天发誓，我对您绝无任何遐想！”\r\n顺便嘟囔句……\r\n也不知是哪条狗妖言惑众。\r\n只听耳边传来啪的一声，男人手中签字笔硬生生折成两段。\r\n四目相对，室内温度骤降。\r\n许久，雷枭薄唇微动。\r\n“汪……”\r\n“……”神经病！\r                    ', '//bookcover.yuewen.com/qdbimg/349573/c_6972481904230701/90')]
        sql = "INSERT INTO `books` (`book_Id`, `book_name`, `state`, `author`, `chan_name`, `synoptic`, `img_url`) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE book_Id = VALUES(book_Id), book_name = VALUES(book_name), state = VALUES(state), author = VALUES(author), chan_name = VALUES(chan_name), synoptic = VALUES(synoptic), img_url = VALUES(img_url) "
        return self.batchAdd(sql, data_info)

    # 获取书本数据
    def getBooksInfo(self):
        booksInfo = []
        booksData = self.parseWithXpath().copy()
        for i in booksData:
            booksInfo.append(
                (i['book_Id'], i['book_name'], i['state'], i['author'], i['chan_name'], i['synoptic'], i['img_url']))
        return booksInfo

    # 调度
    def contents_load(self):
        getBooksInfoData = self.getBooksInfo()

        getBooksInfoRes = self.saveBooks(getBooksInfoData)

        for i in getBooksInfoData:
            print('\tbookId： %s \t书名： 《%s》 \t作者： %s \t状态： %s \t分类： %s \n\t图片： %s ' % (i[0], i[1], i[3], i[2], i[4], i[6]))

        if not getBooksInfoRes:
            print('书籍信息存储失败', getBooksInfoData)


if __name__ == '__main__':
    book = load_book('http://www.xs8.cn', 5)
    print(book.b_link)
    book.contents_load()
