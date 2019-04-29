#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬取新浪读书'
__author__ = 'Mad Dragon'
__mtime__ = '2019/4/28'
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
import math
import time
from urllib.parse import urlencode

import pymysql
import redis
import requests
from lxml import etree


class Data(object):
    def bytes_to_str(s, encoding='utf-8'):
        """Returns a str if a bytes object is given."""
        if isinstance(s, bytes):
            return s.decode(encoding)
        return s

    def groupingData(self, list, pageSize, fixed=False):
        listSize = len(list)
        if fixed:
            listGroupSize = pageSize
        else:
            listGroupSize = math.ceil(float(listSize) / pageSize)

        nloops = range(listGroupSize)
        listTaskList = []
        listTaskSize = math.ceil(float(listSize) / listGroupSize)
        for i in nloops:
            try:
                print("第 %s 组 ：[ %s ] \n\t" % (i + 1, len(list[i * listTaskSize:(i + 1) * listTaskSize])))
                listTaskList.append(list[i * listTaskSize:(i + 1) * listTaskSize])
            except:
                print("第 %s 组 ：[ %s ] \n\t" % (i + 1, len(list[i * listTaskSize:])))
                listTaskList.append(list[i * listTaskSize:])
        res = {
            'listSize': listSize,
            'listGroupSize': listGroupSize,
            'listTaskSize': listTaskSize,
            'listTaskList': listTaskList
        }
        # print('groupingData : %s' % res)
        return res


class Redis(object):
    def __init__(self):
        self._connection_pool_ = redis.ConnectionPool(
            host=config['redis']['host'],
            port=config['redis']['port'],
            db=config['redis']['db']
        )
        self.r = redis.Redis(connection_pool=self._connection_pool_)
        self.p = redis.StrictRedis(connection_pool=self._connection_pool_)

    # 获取 并 删除 列表某些元素
    def getListData(self, name="list_name1", num=1):
        dataList = []
        for i in range(int(num)):
            try:
                data = self.r.lpop(name)
            except:
                data = None
                print('├  [ DEBUG INFO ] [ getListData ] Redis 服务器炸了。。。。%s , %s' % (name, num))
            if data != None:
                nData = Data.bytes_to_str(data, 'utf-8')
                dataList.append(nData)
        return dataList

    # 批量添加列表
    def setListData(self, name='list_name1', lists=[]):
        if len(lists) <= 0:
            return False
        try:
            self.r.rpush(name, *lists)
            return True
        except:
            print('├  [ DEBUG INFO ] [ setListData ] Redis 服务器炸了。。。。')
            return False


class BaseMySql(object):
    # 数据库信息

    def openMySqlConfig(self):
        return pymysql.connect(config['mysql']['host'], config['mysql']['user'], config['mysql']['password'],
                               config['mysql']['database'])

    def batchAdd(self, sql, data_info):
        db = self.openMySqlConfig()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # # 执行sql语句
        # cursor.executemany(sql, data_info)
        #
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


class MySql(BaseMySql):
    # 获取 单个 书籍id
    def get_book_id_tup(self, book_id, platform, platform_src):
        sql = 'SELECT id FROM book WHERE book_id= %d AND platform = "%s" AND platform_src = "%s"' % (
            int(book_id), platform, platform_src)
        return self.getListData(sql=sql)

    # 获取 单个 章节id
    def get_book_catalog_id_tup(self, book_id, catalog_id):
        sql = 'SELECT id FROM catalogs WHERE book_id= %d AND catalog_id = "%s"' % (int(book_id), catalog_id)
        return self.getListData(sql=sql)

    # 获取 书籍的章节id列表（id,平台章节id） ，用于比对章节是否已经 存在数据库
    def get_book_catalog_data_list_tup(self, book_id):
        sql = 'SELECT id,catalog_id from catalogs WHERE book_id= %d ' % int(book_id)
        return self.getListData(sql=sql)

    # 获取 书籍的章节内容id列表（id,平台章节id） ，用于比对章节内容是否已经 存在数据库
    def get_book_catalog_txt_data_list_tup(self, book_id):
        sql = 'SELECT id,catalog_id from txt WHERE book_id= %d ' % int(book_id)
        return self.getListData(sql=sql)

    # 获取 单个 章节内容的 id
    def get_book_catalog_txt_id_tup(self, catalog_id):
        sql = 'SELECT id FROM txt WHERE catalog_id= %d ' % (int(catalog_id))
        return self.getListData(sql=sql)

    # 保存书籍信息
    def save_book_info_to_mysql(self, data_info):
        sql = "INSERT INTO `book` (`id`, `book_id`, `src`,`title`,`img_url`,`state`,`author`,`chan_name`,`sub_name`,`chapter_total_cnt`,`gender`,`synoptic`,`platform`,`platform_src`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), book_id = VALUES (book_id), src = VALUES (src),title = VALUES (title),img_url = VALUES (img_url),state = VALUES (state),author = VALUES (author),chan_name = VALUES (chan_name),sub_name = VALUES (sub_name),chapter_total_cnt = VALUES (chapter_total_cnt),gender = VALUES (gender),synoptic = VALUES (synoptic),platform = VALUES (platform),platform_src = VALUES (platform_src), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

    # 保存免费书籍信息
    def save_free_book_info_to_mysql(self, data_info):
        sql = "INSERT INTO `book` (`id`, `book_id`, `src`,`title`,`img_url`,`state`,`author`,`chan_name`,`chapter_total_cnt`,`gender`,`synoptic`,`platform`,`platform_src`)  VALUES (%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), book_id = VALUES (book_id), src = VALUES (src),title = VALUES (title),img_url = VALUES (img_url),state = VALUES (state),author = VALUES (author),chan_name = VALUES (chan_name),chapter_total_cnt = VALUES (chapter_total_cnt),gender = VALUES (gender),synoptic = VALUES (synoptic),platform = VALUES (platform),platform_src = VALUES (platform_src), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

    # 保存 章节 信息
    def save_book_catalog_to_mysql(self, data_info):
        sql = "INSERT INTO `catalogs` (`id`,`catalog_id`,`title`, `src`,`book_id`,`book_title`,`cnt`,`uuid`,`vs`,`vn`,`update_time`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id),catalog_id = VALUES (catalog_id),title = VALUES (title), src = VALUES (src),book_id = VALUES (book_id),book_title = VALUES (book_title),cnt = VALUES (cnt),uuid = VALUES (uuid),vs = VALUES (vs),vn = VALUES (vn),update_time = VALUES (update_time), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

    # 保存 章节内容信息
    def save_book_catalog_txt_to_mysql(self, data_info):
        sql = "INSERT INTO `txt` (`id`, `catalog_id`, `catalog_title`,`book_id`,`book_title`,`article`)  VALUES (%s,%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), catalog_id = VALUES (catalog_id), catalog_title = VALUES (catalog_title), book_id = VALUES (book_id), book_title = VALUES (book_title),article = VALUES (article), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)


class Novel(object):
    def __init__(self):
        self._mysql_ = MySql()
        self._data_ = Data()
        self._r_ = Redis()

    # 工具类：通过xpath 解析html
    def analysis_html(self, html, xpath):
        info_obj = {}
        for key, value in xpath.items():
            info_obj[key] = html.xpath(value)
        return info_obj

    def from_list_get_id(self, id_list, id):
        nid = 0
        if (len(id_list)) <= 0:
            return nid
        for item in id_list:
            if id in item:
                nid = item[0]
        return nid

    def get_book_id(self, book_id, platform, platform_src):
        id_tup = self._mysql_.get_book_id_tup(book_id, platform, platform_src)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0

    def get_book_catalog_id(self, book_id, catalog_id):
        id_tup = self._mysql_.get_book_catalog_id_tup(book_id, catalog_id)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0

    def get_book_catalog_txt_id(self, catalog_id):
        id_tup = self._mysql_.get_book_catalog_txt_id_tup(catalog_id)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0


class Novel(object):
    def __init__(self):
        self._mysql_ = MySql()
        self._data_ = Data()
        self._r_ = Redis()

    # 工具类：通过xpath 解析html
    def analysis_html(self, html, xpath):
        info_obj = {}
        for key, value in xpath.items():
            info_obj[key] = html.xpath(value)
        return info_obj

    def from_list_get_id(self, id_list, id):
        nid = 0
        if (len(id_list)) <= 0:
            return nid
        for item in id_list:
            if id in item:
                nid = item[0]
        return nid

    def get_book_id(self, book_id, platform, platform_src):
        id_tup = self._mysql_.get_book_id_tup(book_id, platform, platform_src)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0

    def get_book_catalog_id(self, book_id, catalog_id):
        id_tup = self._mysql_.get_book_catalog_id_tup(book_id, catalog_id)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0

    def get_book_catalog_txt_id(self, catalog_id):
        id_tup = self._mysql_.get_book_catalog_txt_id_tup(catalog_id)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0


class Spider(Novel):
    # 2、访问小说列表页 拿到小说列表
    def get_book_list(self, url, book_list_html_xpath):
        html_list = []
        flip_flag = True
        i = 1
        while flip_flag:
            print('├  请求书籍列表：【 %s 】  请求 ' % (str(url)))
            time.sleep(3)
            try:
                response = requests.get(url=url)
                xml = etree.HTML(response.text)  # 整理成xml文档对象
                html_list = xml.xpath(book_list_html_xpath)
                if len(html_list) > 0:
                    flip_flag = False
                    break
            except:
                pass

            print("├  请求书籍列表：【 %s 】  请求  ==》 失败 ==>  10 秒后再试" % (str(url)))
            i += 1
            time.sleep(10)
            if i > 30:
                self._r_.setListData(name='get_book_list', lists=[str(url)])
                flip_flag = False

        print(url, book_list_html_xpath)
        return html_list


class SpiderModel(Spider):
    # 1、处理模式 1 一条龙（创建小说列表页链接->小说->存储小说->章节->存储章节->内容->存储内容->翻页->小说）
    def run_a_dragon(self, info, xpath, book_list_html_xpath):
        info = eval(info)
        # print(info)
        start = time.time()
        # 1. 请求页面 获取数据
        html_list = self.get_book_list(url=info['src'], book_list_html_xpath=book_list_html_xpath)
        print(html_list)
        if len(html_list) <= 0:
            time.sleep(10)
            print('├  [DEBUG INFO]: 页面数据没有拿到。。。')
            self._r_.setListData(name='book_page_list', lists=[str(info)])
            return []
        end = time.time()
        print('├  消耗时间     ：%s 秒' % (int(float(end) - float(start))))


class Run(SpiderModel):
    def creat_book_page_url_list_to_redis(self, params):
        book_page_list = []
        for item in params:
            gender = item['gender']
            maxPageSize = int(item['maxPageSize']) + 1
            src = item['src']
            cate_id = item['cate_id']
            for id in cate_id:
                for pageSize in range(1, maxPageSize):
                    book_page_list.append(str({
                        'src': src.format(id, pageSize),
                        'gender': gender,
                        'platform': platform,
                        'platform_src': platform_src
                    }))
        groupData = self._data_.groupingData(list=book_page_list, pageSize=1000)
        for item in groupData['listTaskList']:
            self._r_.setListData(name='book_page_url_list', lists=item)

    def a_dragon(self, xpath, book_list_html_xpath, num=1, maxNum=43200):
        flip_flag = True
        i = 1
        while flip_flag:
            start = time.time()
            book_page_url_list = self._r_.getListData(name="book_page_url_list", num=num)
            if len(book_page_url_list) > 0:
                i = 1
                print('├  获取书籍列表链接 %s' % book_page_url_list)
                for info in book_page_url_list:
                    self.run_a_dragon(info=info, xpath=xpath, book_list_html_xpath=book_list_html_xpath)
            else:
                if i < maxNum:
                    print('├  暂无数据 【 %s 】 60 秒后继续' % i)
                    i += 1
                    time.sleep(60)
                else:
                    flip_flag = False
                    print('├  结束抓取')
            end = time.time()
            print('├  消耗时间     ：%s 秒' % (int(float(end) - float(start))))
            print('├  抓取频率过快 180 秒后继续')
            time.sleep(180)

        print('├  结束抓取')


if __name__ == '__main__':
    platform = "新浪读书"
    platform_src = "http://vip.book.sina.com.cn"
    config = {
        "mysql": {
            'host': '172.30.34.155',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'novel_dev'
        },
        "redis": {
            'host': '172.30.34.155',
            'port': 6379,
            'db': 8
        },
        'xpath': {
            'book_id_list': './div[@class="book-mid-info"]/h4/a/@data-bid',
            'src_list': './div[@class="book-mid-info"]/h4/a/@href',
            'title_list': './div[@class="book-mid-info"]/h4/a/text()',
            'img_url_list': './div[@class="book-img-box"]/a/img/@src',
            'state_list': './div[@class="book-mid-info"]/p[@class="author"]/span[1]/text()',
            'author_list': './div[@class="book-mid-info"]/p[@class="author"]/a[1]/text()',
            'chan_name_list': './div[@class="book-mid-info"]/p[@class="author"]/a[2]/text()',
            'sub_name_list': './div[@class="book-mid-info"]/p[@class="author"]/a[3]/text()',
            'synoptic_list': './div[@class="book-mid-info"]/p[@class="intro"]/text()',
        },
        'book_list_html_xpath': '//div[@class="book_list"]/ul//li',
        'freeXpath': {
            'book_id_list': './div[@class="book-mid-info"]/h4/a/@data-bid',
            'src_list': './div[@class="book-mid-info"]/h4/a/@href',
            'title_list': './div[@class="book-mid-info"]/h4/a/text()',
            'img_url_list': './div[@class="book-img-box"]/a/img/@src',
            'state_list': './div[@class="book-mid-info"]/p[@class="author"]/span[1]/text()',
            'author_list': './div[@class="book-mid-info"]/p[@class="author"]/a[1]/text()',
            'chan_name_list': './div[@class="book-mid-info"]/p[@class="author"]/a[2]/text()',
            'synoptic_list': './div[@class="book-mid-info"]/p[@class="intro"]/text()',
        },
        'free_book_list_html_xpath': '//*[@id="limit-list"]/div/ul//li',
        'saveBookCatalogInfoType': 'mysql',  # mysql redis
        'requests_url': [
            'https://www.qidian.com/all',
            'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1000'
        ],
        'freeBookUrl': 'https://www.qidian.com/free',
        'params': [
            {
                'src': 'http://vip.book.sina.com.cn/weibobook/cate.php?cate_id={0}&w=0&s=0&order=1&vt=4&page={1}',
                'maxPageSize': 10000,
                'gender': 1,
                'cate_id': [
                    1036,
                    1003,
                    1001,
                    1035,
                    1009,
                    1002,
                    1031,
                    1042
                ]
            },
            {
                'src': 'http://vip.book.sina.com.cn/weibobook/cate.php?cate_id={0}&w=0&s=0&order=1&vt=4&page={1}',
                'maxPageSize': 10000,
                'gender': 2,
                'cate_id': [
                    1006005,
                    1006003,
                    1007,
                    1006004,
                    1006006,
                    1006007,
                    1043
                ]
            },
            {
                'src': 'http://vip.book.sina.com.cn/weibobook/cate.php?cate_id={0}&w=0&s=0&order=1&vt=4&page={1}',
                'maxPageSize': 10000,
                'gender': 3,
                'cate_id': [
                    50,
                    13,
                    48,
                    3,
                    22,
                    4
                ]
            },
        ]
    }
    # online dev
    environment = 'dev'
    spiderType = 1
    isRepeat = True
    isVs = True
    isDebugger = True

    if environment == 'online':
        config["mysql"]["database"] = 'novel_online'
        config["redis"]["db"] = 12

    # gender = 1  # 性别 1:男 2: 女 3:出版
    xpath = config['xpath']
    book_list_html_xpath = config['book_list_html_xpath']
    requests_url = config['requests_url']

    run = Run()
    if spiderType == 0:
        # 初始化书籍，列表链接池  all :  210000
        print('├  初始化书籍，列表链接池  all :  210000')
        params = config['params']
        run.creat_book_page_url_list_to_redis(params=params)
    elif spiderType == 1:
        # 一条龙服务
        print('├  一条龙服务')
        run.a_dragon(xpath=xpath, book_list_html_xpath=book_list_html_xpath, num=1, maxNum=43200)
