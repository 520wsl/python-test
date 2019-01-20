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
import pymysql
import time
from lxml import etree
import math
import threading
import random


class load_book(object):
    def __init__(self, host, pageSize, gender, loops, maxErrorSize):
        self.b_host = host
        self.b_pageSize = pageSize
        self.b_loops = loops
        self.b_gender = gender
        self.b_pageCount = self.b_pageCount_load()
        self.b_links = self.b_links_load()
        self.content = []
        self.mysql_ip = "172.30.34.210"
        self.mysql_user = "root"
        self.mysql_pwd = "root"
        self.mysql_database = "pythonTest"
        self.maxErrorSize = maxErrorSize
        self.errorSize = 0
        self.okNum = 0
        self.errorurls = []

    # 获取总页数
    def b_pageCount_load(self):
        link = self.b_link_load(1)
        html = etree.HTML(self.getHtmlText(link))
        data_total = html.xpath('//*[@id="page-container"]/@data-total')[0]
        count = math.ceil(float(data_total) / self.b_pageSize)
        return count
        # return 100

    # 生成连接池
    def b_links_load(self):
        links = []
        for pageNum in range(self.b_pageCount):
            links.append(self.b_link_load(pageNum + 1))
        return links

    # 链接处理
    def b_link_load(self, pageNum):
        # https://www.xs8.cn/all?pageSize=10&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=1
        return self.b_host + '/all?pageSize=' + str(
            self.b_pageSize) + '&gender=' + str(
            self.b_gender) + '&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=' + str(
            pageNum)

    # 抓取页面元素
    def getHtmlText(self, url):
        heads = {}
        heads['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        heads['Accept - Encoding'] = 'gzip, deflate, br'
        heads['Accept - Language'] = 'zh-CN,zh;q=0.9'
        heads['Cookie'] = 'newstatisticUUID=1546996330_2089765158; qdrs=0%7C3%7C0%7C0%7C1; qdgd=1'
        heads['Host'] = self.b_host[7:]
        heads[
            'Referer'] = 'https://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=1'
        heads[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        heads['X - Requested - With'] = 'XMLHttpRequest'

        try:
            r = requests.get(url, headers=heads)
            r.encoding = "utr-8"
            return r.text
        except:
            print("获取列表失败,一秒后重试，失败链接：", url)
            time.sleep(1)

    # 解析页面元素
    def parseWithXpath(self, html_text):
        html = etree.HTML(html_text)
        content_list = html.xpath('//div[@class="right-book-list"]//li')
        content = []
        for item in content_list:
            book_Id = item.xpath('.//div[@class="book-info"]/h3/a/@href')[0][6:]
            book_name = item.xpath('.//div[@class="book-info"]/h3/a/text()')[0]
            author = item.xpath('.//div[@class="book-info"]/h4/a/text()')[0]
            tag = item.xpath('.//div[@class="book-info"]/p[@class="tag"]/span/text()')
            synoptic = item.xpath('.//div[@class="book-info"]/p[@class="intro"]/text()')[0]
            img_url = item.xpath('.//div[@class="book-img"]/a/img/@src')[0]
            chan_name = tag[0]
            state = tag[1]
            content.append({
                'book_Id': book_Id,
                'book_name': book_name,
                'state': state,
                'author': author,
                'chan_name': chan_name,
                'synoptic': str(synoptic),
                'img_url': img_url
            })
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
        sql = "INSERT INTO `books` (`book_Id`, `book_name`, `state`, `author`, `chan_name`, `synoptic`, `img_url`,`gender`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE book_Id = VALUES(book_Id), book_name = VALUES(book_name), state = VALUES(state), author = VALUES(author), chan_name = VALUES(chan_name), synoptic = VALUES(synoptic), img_url = VALUES(img_url), gender = VALUES(gender) "
        return self.batchAdd(sql, data_info)

    # 获取书本数据
    def getBooksInfo(self, booksData):
        booksInfo = []
        for i in booksData:
            booksInfo.append(
                (i['book_Id'], i['book_name'], i['state'], i['author'], i['chan_name'], str(i['synoptic']),
                 i['img_url'], self.b_gender))
        return booksInfo

    # 获取 没页数据 并 存入数据库
    def item_get_and_save(self, link, group, num):
        content = self.parseWithXpath(self.getHtmlText(link))
        getBooksInfoData = self.getBooksInfo(content)
        # self.content.append(getBooksInfoData)
        print("\t\t第 %d 组链接， 第 %d 条链接 [ %s ] 抓取完成...【  %s  】\n" % (group, num, link, len(getBooksInfoData)))
        if len(getBooksInfoData) < self.b_pageSize and len(getBooksInfoData) <= 2:
            self.errorurls.append(link)
        time.sleep(random.randint(10, 15))
        self.write_txt(getBooksInfoData, link, group, num)

    # 按组获取
    def section_load(self, links, group):
        if len(links) <= 0:
            return;
        print('\t第 %d 组链接， 开始 抓取。。。\n' % (group))

        i = 0
        for link in links:
            i += 1
            time.sleep(random.randint(20, 30))
            self.item_get_and_save(link, group, i)

    # 调度
    def contents_load(self):
        threads = []
        nloops = range(self.b_loops)
        task_list = []
        task_size = math.ceil(float(len(self.b_links)) / self.b_loops)
        print("网站：%s" % self.b_host)
        print("\t网站 共有 %s 页小说，每页 %s 本小说 。\n" % (self.b_pageCount, self.b_pageSize))
        print("\t预计总共抓取小说 %s  本。\n" % (self.b_pageCount * self.b_pageSize))

        print('\t%s 条链接， 共分为 %s 个线程组 , 每组线程 %s 条链接。 \n' % (len(self.b_links), self.b_loops, task_size))

        for i in nloops:
            # print(i)
            # print(i * task_size)
            # print((i + 1) * task_size)
            # print(self.b_links[i * task_size:(i + 1) * task_size])
            # print(self.b_links[i * task_size:])
            try:
                print("\t\t\t第 %s 组 ：%s" % (i + 1, str(self.b_links[i * task_size:(i + 1) * task_size])))
                task_list.append(self.b_links[i * task_size:(i + 1) * task_size])
            except:
                print("\t\t\t第 %s 组 ：%s" % (i + 1, str(self.b_links[i * task_size:])))
                task_list.append(self.b_links[i * task_size:])
        # print(threads)
        # print(nloops)
        # print(task_list)
        # print(task_size)
        for i in nloops:
            if len(task_list[i]) <= 0:
                continue
            # print(task_list[i])
            t = threading.Thread(target=self.section_load, args=(task_list[i], (i + 1)))
            threads.append(t)

        for i in nloops:
            if len(task_list[i]) <= 0:
                continue
            print('\n开启第 %s 线程...' % (i + 1))
            threads[i].start()

        for i in nloops:
            if len(task_list[i]) <= 0:
                continue
            threads[i].join()

    def write_txt(self, getBooksInfoData, link, group, num):
        print("\t\t第 %d 组链接， 第 %d 条链接 [ %s ] : ==> 开始 存储 链接内容...\n" % (group, num, link))
        getBooksInfoRes = self.saveBooks(getBooksInfoData)
        if not getBooksInfoRes:
            print('\t书籍信息存储失败')
        else:
            self.okNum += 1
            print("\t\t第 %d 组链接， 第 %d 条链接 [ %s ] : ==> \t存储成功 %d 条 小说！\n" % (group, num, link, len(getBooksInfoData)))

    def setLinks(self):
        self.errorSize += 1
        self.b_links = self.errorurls.copy()
        print('\t\t存在失败链接 %s 条， 现在 【第 %s 次  】  重新抓取失败链接' % (len(self.errorurls), self.errorSize))
        print(self.errorurls)
        self.errorurls = []
        self.contents_load()
        self.isOK()

    def isOK(self):
        if self.errorSize >= self.maxErrorSize:
            return;

        if len(self.errorurls) > 0:
            self.setLinks()


if __name__ == '__main__':
    book = load_book('http://www.xs8.cn', 500, 1, 10, 20)
    '''
        load_book
            网址
            分页大小
            男女 ：1男 2女
            线程数
            失败重新抓取次数
    '''
    book.contents_load()
    book.isOK()
    print('成功抓取链接 %s 条' % book.okNum)
    print('失败链接 %d 条：\n' % len(book.errorurls))
    print(book.errorurls)
