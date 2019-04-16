#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬取起点小说'
__author__ = 'Mad Dragon'
__mtime__ = '2019/4/16'
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
import json
import logging
import time

import moment
import pymysql
import redis
import requests
from lxml import etree

url = "https://www.qidian.com/all"
header = {
    "Host": "www.zhipin.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
gender = 1  # 性别 1:男 2: 女
platform = "起点中文网"
platform_src = "https://www.qidian.com"
book_key = ['BookImgSrc', 'BookTit', 'BookTitSrc', 'BookAuthor', 'BookAuthorSrc', 'BookAuthorChanName',
            'BookAuthorSubName', 'BookState', 'BookSynoptic', 'bookGender']
host = '192.168.2.202'
port = 6379
db = 8

mysql = {
    'host': '172.30.34.210',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'novel_dev'
}


class Spider(object):

    def __init__(self):
        self.r = redis.Redis(connection_pool=redis.ConnectionPool(host=host, port=port, db=db))

    def get_book_list(self):
        request_url = url

        flip_flag = True

        while flip_flag:
            print("[DEBUG INFO]: 请求网址： {}".format(request_url))
            # 1. 请求一级页面拿到数据， 抽取小说名、小说链接、小说封面、小说作者、类型、小说进度状态、小说简介
            try:
                response = requests.get(url=request_url)
                xml = etree.HTML(response.text)  # 整理成xml文档对象
                book_list = xml.xpath('//ul[@class="all-img-list cf"]//li')
                for info in book_list:
                    book_img_src_list = info.xpath('./div[@class="book-img-box"]/a/img/@src')

                    book_tit_list = info.xpath('./div[@class="book-mid-info"]/h4/a/text()')
                    book_tit_src_list = info.xpath('./div[@class="book-mid-info"]/h4/a/@href')
                    book_id_list = info.xpath('./div[@class="book-mid-info"]/h4/a/@data-bid')

                    book_author_list = info.xpath('./div[@class="book-mid-info"]/p[@class="author"]/a[1]/text()')
                    book_author_src_list = info.xpath('./div[@class="book-mid-info"]/p[@class="author"]/a[1]/@href')

                    book_chan_name_list = info.xpath('./div[@class="book-mid-info"]/p[@class="author"]/a[2]/text()')
                    book_sub_name_list = info.xpath('./div[@class="book-mid-info"]/p[@class="author"]/a[3]/text()')

                    book_state_list = info.xpath('./div[@class="book-mid-info"]/p[@class="author"]/span[1]/text()')
                    book_synoptic_list = info.xpath('./div[@class="book-mid-info"]/p[@class="intro"]/text()')

                    book_gender_list = [gender]
                    platform_list = [platform]
                    platform_src_list = [platform_src]

                    for item in zip(book_img_src_list, book_tit_list,
                                    book_tit_src_list, book_author_list,
                                    book_author_src_list, book_chan_name_list,
                                    book_sub_name_list, book_state_list,
                                    book_synoptic_list, book_gender_list,
                                    book_id_list, platform_list,
                                    platform_src_list):
                        book_content = self.next_file(bookId=list(item)[10])
                        book_chapter_total_cnt = book_content['chapterTotalCnt']
                        vs = book_content['vs']
                        book_catalog = self.get_catalog(vs)

                        book_info = {
                            'book_img_src': list(item)[0],
                            'book_tit': list(item)[1],
                            'book_tit_src': list(item)[2],
                            'book_author': list(item)[3],
                            'book_author_src': list(item)[4],
                            'book_chan_name': list(item)[5],
                            'book_sub_name': list(item)[6],
                            'book_state': list(item)[7],
                            'book_synoptic': list(item)[8],
                            'book_gender': list(item)[9],
                            "book_id": list(item)[10],
                            "platform": list(item)[11],
                            "platform_src": list(item)[12],
                            "book_catalog": book_catalog,
                            "book_chapter_total_cnt": book_chapter_total_cnt
                        }
                        # print(book_info)
                        book_id = self.save_info_to_mysql(book_info)
                        self.save_catalog_to_mysql(book_id, book_info)
                try:
                    next_src = xml.xpath('//*[@id="page-container"]/div/ul/li[last()]/a/@href')
                    if len(next_src) > 0:
                        request_url = "https:" + next_src[0]
                    else:
                        self.setListData(name='bookListErrorSrc', lists=[request_url])
                        flip_flag = False
                except:
                    self.setListData(name='bookListErrorSrc', lists=[request_url])
                    flip_flag = False
            except:
                self.setListData(name='bookListErrorSrc', lists=[request_url])
                flip_flag = False

    def get_catalog(self, vs):
        links = []
        for i in vs:
            for j in i['cs']:
                links.append({
                    'vS': i['vS'],
                    'vN': i['vN'],
                    'cN': j['cN'],
                    'cU': j['cU'],
                    'cnt': j['cnt'],
                    'uT': j['uT'],
                    'uuid': j['uuid'],
                    'id': j['id']
                })
        return links

    def next_file(self, bookId):
        request_url = "https://read.qidian.com/ajax/book/category?_csrfToken=&bookId=" + bookId
        print("next_file:请求的URL： {}".format(request_url))
        try:
            response = requests.get(url=request_url)
            response.encoding = "utr-8"
            category = json.loads(response.text)
            if len(category['data']) > 0:
                return category['data']
            else:
                return {}
        except:
            self.setListData(name='bookCatalogErrorSrc', lists=[request_url])

    def setListData(self, name='bookList', lists=[]):
        if len(lists) <= 0: return;
        self.r.rpush(name, *lists)

    # 数据库信息
    def openMySqlConfig(self):
        return pymysql.connect(mysql['host'], mysql['user'], mysql['password'], mysql['database'])

    def get_book_catalog_id(self, book_Id, book_tit, catalog_id, title):
        get_book_catalog_id_mysql = 'SELECT id FROM catalogs WHERE book_Id= %d AND book_title= "%s" AND catalog_id = "%s" AND title = "%s"' % (
            int(book_Id), book_tit, catalog_id, title)
        return self.getListData(get_book_catalog_id_mysql)

    def get_book_id(self, book_Id, title, platform, platform_src):
        get_book_id_mysql = 'SELECT id FROM book WHERE book_Id= %d AND title= "%s" AND platform = "%s" AND platform_src = "%s"' % (
            int(book_Id), title, platform, platform_src)
        return self.getListData(get_book_id_mysql)

    def batchAdd(self, sql, data_info):
        # print(sql, data_info)
        db = self.openMySqlConfig()
        # print(db)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # print(cursor)

        # # 执行sql语句
        # cursor.executemany(sql, data_info)
        # print('aa')
        # # 提交到数据库执行
        # db.commit()
        # db.close()
        # return True

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

    def getListData(self, sql):
        db = self.openMySqlConfig()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        res = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        return res

    def save_catalog_to_mysql(self, book_id, book_info):
        # print(book_info)
        if book_id <= 0:
            book_id_tup = self.get_book_id(book_info['book_id'], book_info['book_tit'], book_info['platform'],
                                           book_info['platform_src'])
            if len(book_id_tup) > 0:
                book_id = book_id_tup[0][0]

        for item in book_info['book_catalog']:
            catalog_id = self.get_book_catalog_id(book_id, book_info['book_tit'], item['id'], item['cN'])
            if len(catalog_id) > 0:
                id = catalog_id[0][0]
            else:
                id = 0

            # print('***************>')
            # print(item['cN'])
            # print(item['id'])
            # print(book_id)
            # print(book_info['book_tit'])
            # print(id)

            save_book_info_data = []
            save_book_catalog_mysql = "INSERT INTO `catalogs` (`id`,`catalog_id`,`title`, `src`,`book_Id`,`book_title`,`cnt`,`uuid`,`vs`,`vn`,`update_time`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id),catalog_id = VALUES (catalog_id),title = VALUES (title), src = VALUES (src),book_Id = VALUES (book_Id),book_title = VALUES (book_title),cnt = VALUES (cnt),uuid = VALUES (uuid),vs = VALUES (vs),vn = VALUES (vn),update_time = VALUES (update_time), nex = nex+1"
            save_book_info_data.append((
                id, item['id'], item['cN'], item['cU'], book_id, book_info['book_tit'],
                item['cnt'], item['uuid'], item['vS'], item['vN'], item['uT']
            ))

            save_book_catalog_res = self.batchAdd(save_book_catalog_mysql, save_book_info_data)
            if save_book_catalog_res:
                print('书本 【 %s 】| book_id 【 %s 】  章节 【 %s 】| catalog_id 【 %s 】  保存成功' % (
                    book_info['book_tit'], book_id, item['cN'], id))
            else:
                print('书本 【 %s 】| book_id 【 %s 】  章节 【 %s 】| catalog_id 【 %s 】  保存失败' % (
                    book_info['book_tit'], book_id, item['cN'], id))
                self.setListData(name='saveBookCatalogDataError', lists=[save_book_catalog_mysql, save_book_info_data])

    def save_info_to_mysql(self, book_info):
        # print(book_info)
        save_book_info_data = []
        book_id = self.get_book_id(book_info['book_id'], book_info['book_tit'], book_info['platform'],
                                   book_info['platform_src'])
        save_book_info_mysql = "INSERT INTO `book` (`id`, `book_Id`, `src`,`title`,`img_url`,`state`,`author`,`chan_name`,`sub_name`,`chapter_total_cnt`,`gender`,`synoptic`,`platform`,`platform_src`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), book_Id = VALUES (book_Id), src = VALUES (src),title = VALUES (title),img_url = VALUES (img_url),state = VALUES (state),author = VALUES (author),chan_name = VALUES (chan_name),sub_name = VALUES (sub_name),chapter_total_cnt = VALUES (chapter_total_cnt),gender = VALUES (gender),synoptic = VALUES (synoptic),platform = VALUES (platform),platform_src = VALUES (platform_src), nex = nex+1"
        # book_id = 0 # 测试用
        # "book_catalog": book_catalog,
        if len(book_id) > 0:
            id = book_id[0][0]
        else:
            id = 0

        # print(id)

        save_book_info_data.append((
            id, book_info['book_id'], book_info['book_tit_src'], book_info['book_tit'],
            book_info['book_img_src'],
            book_info['book_state'], book_info['book_author'], book_info['book_chan_name'],
            book_info['book_sub_name'],
            book_info['book_chapter_total_cnt'], book_info['book_gender'], book_info['book_synoptic'],
            book_info['platform'], book_info['platform_src']))

        save_book_info_res = self.batchAdd(save_book_info_mysql, save_book_info_data)
        if save_book_info_res:
            print('书本 【 %s 】| book_id 【 %s 】 保存成功' % (book_info['book_tit'], id))
        else:
            print('书本 【 %s 】| book_id 【 %s 】  保存失败' % (book_info['book_tit'], id))
            self.setListData(name='saveBookInfoDataError', lists=[save_book_info_mysql, save_book_info_data])

        return id


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger():
    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 用字典保存日志级别
        format_dict = {
            1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        }
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


if __name__ == "__main__":
    spider = Spider()
    spider.get_book_list()
