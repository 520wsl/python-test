#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬取起点小说_v2 封装 抽离'
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
import time
import pymysql
import redis
import requests
from lxml import etree

# dev  online
environment = 'online'

# url = "https://www.qidian.com/all"
url = "https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=10"
header = {
    "Host": "www.qidian.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
gender = 1  # 性别 1:男 2: 女
platform = "起点中文网"
platform_src = "https://www.qidian.com"
book_key = ['BookImgSrc', 'BookTit', 'BookTitSrc', 'BookAuthor', 'BookAuthorSrc', 'BookAuthorChanName',
            'BookAuthorSubName', 'BookState', 'BookSynoptic', 'bookGender']
isVs = False
isRepeat = False

config = {
    "mysql": {
        'host': '172.30.34.210',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'novel_dev'
    },
    "redis": {
        'host': '192.168.2.202',
        'port': 6379,
        'db': 8
    },
    'xpath': {
        'book_img_src_list ': './div[@class="book-img-box"]/a/img/@src',
        'book_tit_list ': './div[@class="book-mid-info"]/h4/a/text()',
        'book_tit_src_list ': './div[@class="book-mid-info"]/h4/a/@href',
        'book_author_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[1]/text()',
        'book_author_src_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[1]/@href',
        'book_chan_name_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[2]/text()',
        'book_sub_name_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[3]/text()',
        'book_state_list ': './div[@class="book-mid-info"]/p[@class="author"]/span[1]/text()',
        'book_synoptic_list ': './div[@class="book-mid-info"]/p[@class="intro"]/text()',
        'book_id_list ': './div[@class="book-mid-info"]/h4/a/@data-bid'
    }
}

if environment == 'online':
    isVs = False
    isRepeat = False
    config = {
        "mysql": {
            'host': '172.30.34.210',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'novel_online'
        },
        "redis": {
            'host': '192.168.2.202',
            'port': 6379,
            'db': 12
        },
        'xpath': {
            'book_img_src_list ': './div[@class="book-img-box"]/a/img/@src',
            'book_tit_list ': './div[@class="book-mid-info"]/h4/a/text()',
            'book_tit_src_list ': './div[@class="book-mid-info"]/h4/a/@href',
            'book_author_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[1]/text()',
            'book_author_src_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[1]/@href',
            'book_chan_name_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[2]/text()',
            'book_sub_name_list ': './div[@class="book-mid-info"]/p[@class="author"]/a[3]/text()',
            'book_state_list ': './div[@class="book-mid-info"]/p[@class="author"]/span[1]/text()',
            'book_synoptic_list ': './div[@class="book-mid-info"]/p[@class="intro"]/text()',
            'book_id_list ': './div[@class="book-mid-info"]/h4/a/@data-bid'
        }
    }


class Data(object):
    def bytes_to_str(s, encoding='utf-8'):
        """Returns a str if a bytes object is given."""
        if isinstance(s, bytes):
            return s.decode(encoding)
        return s


class BaseMySql(object):
    # 数据库信息

    def openMySqlConfig(self):
        return pymysql.connect(config['mysql']['host'], config['mysql']['user'], config['mysql']['password'],
                               config['mysql']['database'])

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
    def get_book_id_tup(self, book_Id, platform, platform_src):
        sql = 'SELECT id FROM book WHERE book_Id= %d AND platform = "%s" AND platform_src = "%s"' % (
            int(book_Id), platform, platform_src)
        return self.getListData(sql=sql)

    def get_book_catalog_id_tup(self, book_Id, catalog_id):
        sql = 'SELECT id FROM catalogs WHERE book_Id= %d AND catalog_id = "%s"' % (int(book_Id), catalog_id)
        return self.getListData(sql=sql)

    def get_book_catalog_txt_id_tup(self, catalog_id):
        sql = 'SELECT id FROM txt WHERE catalog_id= %d ' % (int(catalog_id))
        return self.getListData(sql=sql)

    def save_book_info_to_mysql(self, data_info):
        sql = "INSERT INTO `book` (`id`, `book_Id`, `src`,`title`,`img_url`,`state`,`author`,`chan_name`,`sub_name`,`chapter_total_cnt`,`gender`,`synoptic`,`platform`,`platform_src`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), book_Id = VALUES (book_Id), src = VALUES (src),title = VALUES (title),img_url = VALUES (img_url),state = VALUES (state),author = VALUES (author),chan_name = VALUES (chan_name),sub_name = VALUES (sub_name),chapter_total_cnt = VALUES (chapter_total_cnt),gender = VALUES (gender),synoptic = VALUES (synoptic),platform = VALUES (platform),platform_src = VALUES (platform_src), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

    def save_book_catalog_to_mysql(self, data_info):
        sql = "INSERT INTO `catalogs` (`id`,`catalog_id`,`title`, `src`,`book_Id`,`book_title`,`cnt`,`uuid`,`vs`,`vn`,`update_time`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id),catalog_id = VALUES (catalog_id),title = VALUES (title), src = VALUES (src),book_Id = VALUES (book_Id),book_title = VALUES (book_title),cnt = VALUES (cnt),uuid = VALUES (uuid),vs = VALUES (vs),vn = VALUES (vn),update_time = VALUES (update_time), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

    def save_book_catalog_txt_to_mysql(self, data_info):
        sql = "INSERT INTO `txt` (`id`, `catalog_id`, `catalog_title`,`article`)  VALUES (%s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), catalog_id = VALUES (catalog_id), catalog_title = VALUES (catalog_title),article = VALUES (article), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)


class Redis(object):
    def __init__(self):
        self._connection_pool_ = redis.ConnectionPool(
            host=config['redis']['host'],
            port=config['redis']['port'],
            db=config['redis']['db'])
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
                print('├  [ DEBUG INFO ] [ getListData ] Redis 服务器炸了。。。。')
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
            return True


class Novel(object):
    def __init__(self):
        self._mysql_ = MySql()
        self._data_ = Data()
        self._r_ = Redis()

    def request_api_data(self, request_url):
        print("\t├")
        print("\t├  API ：【 %s 】 请求" % (request_url))
        response = requests.get(url=request_url)
        response.encoding = "utr-8"
        category = json.loads(response.text)
        try:
            return category['data']
        except:
            print("\t├  API ：【 %s 】 请求 ==》 失败 ==> %s" % (request_url, str(category)))
            self._r_.setListData(name='request_api_data', lists=[str(request_url + str(category))])
            return {}

    def get_api_data(self, request_url):
        category_data = {}
        flip_flag = True
        i = 1
        while flip_flag:
            category_data = self.request_api_data(request_url=request_url)
            if len(category_data) > 0:
                flip_flag = False
            else:
                print('\t├  第 %s 次请求失败' % i)
                i += 1
                time.sleep(10)
                if i > 30:
                    flip_flag = False
        return category_data

    def get_next_page_path(self, request_url, xpath):
        next_page = ''
        flip_flag = True
        i = 1
        while flip_flag:
            try:
                print("┍")
                print("├  get_next_page_path:  第 {} 次 请求的URL： {}".format(i, request_url))
                response = requests.get(url=request_url)
                xml = etree.HTML(response.text)
                next_src = xml.xpath(xpath)
                if len(next_src) > 0:
                    next_page = "https:" + next_src[0]
                    flip_flag = False
                else:
                    print('\t├  第 %s 次请求失败' % i)
                    i += 1
                    time.sleep(10)
                    if i > 30:
                        flip_flag = False
                        self._r_.setListData(name='get_next_page_path', lists=[str(i, request_url)])
            except:
                print('\t├  第 %s 次请求失败' % i)
                i += 1
                time.sleep(10)
                if i > 30:
                    flip_flag = False
                    self._r_.setListData(name='get_next_page_path', lists=[str(i, request_url)])

        return next_page

    def get_book_id(self, book_Id, platform, platform_src):
        id_tup = self._mysql_.get_book_id_tup(book_Id, platform, platform_src)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0

    def get_book_catalog_id(self, book_Id, catalog_id):
        id_tup = self._mysql_.get_book_catalog_id_tup(book_Id, catalog_id)
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
    def format_book_catalog_info_list(self, data):
        info_list = []
        for i in data:
            for j in i['cs']:
                info_list.append({
                    'vS': i['vS'],
                    'vN': i['vN'],
                    'cN': j['cN'],
                    'cU': j['cU'],
                    'cnt': j['cnt'],
                    'uT': j['uT'],
                    'uuid': j['uuid'],
                    'id': j['id']
                })
        return info_list

    def get_book_catalog_list(self, book_id):
        # request_url = "https://read.qidian.com/ajax/book/category?_csrfToken=&bookId=1012797863"
        request_url = "https://read.qidian.com/ajax/book/category?_csrfToken=&bookId=" + book_id
        book_content = self.get_api_data(request_url=request_url)
        return {
            'book_catalog': self.format_book_catalog_info_list(data=book_content['vs']),
            'book_chapter_total_cnt': book_content['chapterTotalCnt']
        }

    def format_book_info_list(self, info):
        book_info_list = []
        book = {}
        xpath = config['xpath']
        for key, value in xpath.items():
            book[key] = info.xpath(value)

        for item in zip(*book.values()):
            book_info_list.append({
                'book_img_src': list(item)[0],
                'book_tit': list(item)[1],
                'book_tit_src': list(item)[2],
                'book_author': list(item)[3],
                'book_author_src': list(item)[4],
                'book_chan_name': list(item)[5],
                'book_sub_name': list(item)[6],
                'book_state': list(item)[7],
                'book_synoptic': list(item)[8],
                "book_id": list(item)[9],
                'book_gender': gender,
                "platform": platform,
                "platform_src": platform_src
            })
        return book_info_list

    def format_book_list(self, book_list):
        book_info_list = []
        for info in book_list:
            book_info = self.format_book_info_list(info=info)
            for item in book_info:
                book_info_list.append(item)
        return book_info_list

    def get_book_list(self):
        request_url = url
        flip_flag = True

        while flip_flag:
            print("┍")
            print("├  [DEBUG INFO]: 一级页面网址： {}".format(request_url))
            # 1. 请求一级页面拿到数据， 抽取小说名、小说链接、小说封面、小说作者、类型、小说进度状态、小说简介
            try:
                response = requests.get(url=request_url)
                xml = etree.HTML(response.text)  # 整理成xml文档对象
                book_list = xml.xpath('//ul[@class="all-img-list cf"]//li')
                book_info_list = self.format_book_list(book_list=book_list)
                time.sleep(2)
                if len(book_info_list) <= 0:
                    time.sleep(10)
                    print('├  [DEBUG INFO]: 页面数据没有拿到。。。')
                    continue
                for item in book_info_list:
                    book_catalog_list = self.get_book_catalog_list(book_id=item['book_id'])
                    item['book_chapter_total_cnt'] = book_catalog_list['book_chapter_total_cnt']
                    item['book_catalog'] = book_catalog_list['book_catalog']
                    book_id = self.save_info_to_mysql(book_info=item)
                    if book_id > 0:
                        book_catalog_txt_src_info = self.save_catalog_to_mysql(book_id=book_id, book_info=item)
                        for book_catalog_info in book_catalog_txt_src_info:
                            self.finally_file(catalog_id=book_catalog_info['catalog_id'],
                                              catalog_title=book_catalog_info['catalog_title'],
                                              catalog_src=book_catalog_info['catalog_src'], book_tit=item['book_tit'])
                    else:
                        self._r_.setListData(name='book_info_list', lists=[str(item)])

                next_page_xpath = '//*[@id="page-container"]/div/ul/li[last()]/a/@href'
                next_page = self.get_next_page_path(request_url=request_url, xpath=next_page_xpath)
                if len(next_page) > 0:
                    request_url = next_page
                else:
                    flip_flag = False
            except:
                self._r_.setListData(name='bookListErrorSrc', lists=[str(request_url)])
                flip_flag = False

    def save_book_catalog(self, id, item, book_id, book_info, catalog_src):
        save_catalog_data = []
        save_catalog_data.append((
            id, item['id'], item['cN'], catalog_src, book_id, book_info['book_tit'],
            item['cnt'], item['uuid'], item['vS'], item['vN'], item['uT']
        ))
        res = self._mysql_.save_book_catalog_to_mysql(data_info=save_catalog_data)
        if res:
            print('\t\t\t\t\t├')
            print(
                '\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】| catalog_id 【 %s 】  目录保存成功' % (book_info['book_tit'], item['cN'], id))
        else:
            print('\t\t\t\t\t├')
            print('\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】 | catalog_id 【 %s 】  目录保存失败' % (
                book_info['book_tit'], item['cN'], id))
            self._r_.setListData(name='save_book_catalog', lists=[str(save_catalog_data)])
        return res

    def save_catalog_to_mysql(self, book_id, book_info):
        book_catalog_txt_src_info = []
        for item in book_info['book_catalog']:
            id = self.get_book_catalog_id(book_Id=book_id, catalog_id=item['id'])
            catalog_src = item['cU']
            if item['vS'] == 1:
                catalog_src = str(book_info['book_id']) + '/' + str(item['id'])
            if id > 0:
                if isRepeat == False:
                    print('\t\t\t\t\t├')
                    print('\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】 | catalog_id 【 %s 】  已抓取 ==> 跳过' % (
                        book_info['book_tit'], item['cN'], id))
                    continue
            res = self.save_book_catalog(id, item, book_id, book_info, catalog_src)
            if res:
                id = self.get_book_catalog_id(book_Id=book_id, catalog_id=item['id'])
                book_catalog_txt_src_info.append({
                    'catalog_id': id,
                    'catalog_title': item['cN'],
                    'catalog_src': catalog_src
                })
        return book_catalog_txt_src_info

    def finally_file(self, catalog_id, catalog_title, catalog_src, book_tit):
        request_url = ' https://read.qidian.com/chapter/3173393/413059330'
        # request_url = "https://read.qidian.com/chapter/" + catalog_src
        print('\t\t\t\t\t├')
        print("\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】| 内容URL 【 %s 】" % (book_tit, catalog_title, request_url))
        response = requests.get(request_url)
        xml = etree.HTML(response.text)
        article = u"\n".join(xml.xpath('//div[@class="read-content j_readContent"]//p/text()'))
        self.save_catalog_txt_mysql(catalog_id, catalog_title, str(article), book_tit)

    def save_catalog_txt_mysql(self, catalog_id, catalog_title, article, book_tit):
        save_catalog_txt_data = []
        id = self.get_book_catalog_txt_id(catalog_id=catalog_id)
        if id > 0:
            if isRepeat == False:
                print('\t\t\t\t\t├')
                print('\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】 内容 | catalog_id 【 %s 】 已抓取 ==> 跳过' % (
                    book_tit, catalog_title, catalog_id))
                return

        save_catalog_txt_data.append((id, catalog_id, catalog_title, article))
        try:
            save_book_info_res = self._mysql_.save_book_catalog_txt_to_mysql(data_info=save_catalog_txt_data)
            if save_book_info_res:
                print('\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】| catalog_id 【 %s 】| id 【 %s 】 内容保存成功' % (
                    book_tit, catalog_title, catalog_id, id))
            else:
                print('\t\t\t\t\t├  书籍 【 %s 】 章节 【 %s 】| catalog_id 【 %s 】| id 【 %s 】  内容保存失败' % (
                    book_tit, catalog_title, catalog_id, id))
                self._r_.setListData(name='saveCatalogTxtDataError', lists=[str(save_catalog_txt_data)])
        except:
            print('├  [ DEBUG INFO ] [ save_book_info_res ] Redis 存数据炸了。。。。', save_catalog_txt_data)

    def save_info_to_mysql(self, book_info):
        data_info = []
        id = self.get_book_id(book_Id=book_info['book_id'], platform=book_info['platform'],
                              platform_src=book_info['platform_src'])
        data_info.append((
            id, book_info['book_id'], book_info['book_tit_src'], book_info['book_tit'],
            book_info['book_img_src'],
            book_info['book_state'], book_info['book_author'], book_info['book_chan_name'],
            book_info['book_sub_name'],
            book_info['book_chapter_total_cnt'], book_info['book_gender'], book_info['book_synoptic'],
            book_info['platform'], book_info['platform_src']))
        res = self._mysql_.save_book_info_to_mysql(data_info=data_info)
        if res:
            id = self.get_book_id(book_Id=book_info['book_id'], platform=book_info['platform'],
                                  platform_src=book_info['platform_src'])
            print('\t├  书籍 【 %s 】 信息| book_id 【 %s 】 保存成功' % (book_info['book_tit'], id))
        else:
            print('\t├  书籍 【 %s 】 信息 | book_id 【 %s 】 保存失败' % (book_info['book_tit'], id))
            self._r_.setListData(name='saveBookInfoDataError', lists=[str(data_info)])

        return id


if __name__ == "__main__":
    spider = Spider()
    spider.get_book_list()
