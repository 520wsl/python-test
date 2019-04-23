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
    def get_book_id_tup(self, book_id, platform, platform_src):
        sql = 'SELECT id FROM book WHERE book_id= %d AND platform = "%s" AND platform_src = "%s"' % (
            int(book_id), platform, platform_src)
        return self.getListData(sql=sql)

    def get_book_catalog_id_tup(self, book_id, catalog_id):
        sql = 'SELECT id FROM catalogs WHERE book_id= %d AND catalog_id = "%s"' % (int(book_id), catalog_id)
        return self.getListData(sql=sql)

    def get_book_catalog_data_list_tup(self, book_id):
        sql = 'SELECT id,catalog_id from catalogs WHERE book_id= %d ' % int(book_id)
        return self.getListData(sql=sql)

    def get_book_catalog_txt_data_list_tup(self, book_id):
        sql = 'SELECT id,catalog_id from txt WHERE book_id= %d ' % int(book_id)
        return self.getListData(sql=sql)

    def get_book_catalog_txt_id_tup(self, catalog_id):
        sql = 'SELECT id FROM txt WHERE catalog_id= %d ' % (int(catalog_id))
        return self.getListData(sql=sql)

    def save_book_info_to_mysql(self, data_info):
        sql = "INSERT INTO `book` (`id`, `book_id`, `src`,`title`,`img_url`,`state`,`author`,`chan_name`,`sub_name`,`chapter_total_cnt`,`gender`,`synoptic`,`platform`,`platform_src`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id), book_id = VALUES (book_id), src = VALUES (src),title = VALUES (title),img_url = VALUES (img_url),state = VALUES (state),author = VALUES (author),chan_name = VALUES (chan_name),sub_name = VALUES (sub_name),chapter_total_cnt = VALUES (chapter_total_cnt),gender = VALUES (gender),synoptic = VALUES (synoptic),platform = VALUES (platform),platform_src = VALUES (platform_src), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

    def save_book_catalog_to_mysql(self, data_info):
        sql = "INSERT INTO `catalogs` (`id`,`catalog_id`,`title`, `src`,`book_id`,`book_title`,`cnt`,`uuid`,`vs`,`vn`,`update_time`)  VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES (id),catalog_id = VALUES (catalog_id),title = VALUES (title), src = VALUES (src),book_id = VALUES (book_id),book_title = VALUES (book_title),cnt = VALUES (cnt),uuid = VALUES (uuid),vs = VALUES (vs),vn = VALUES (vn),update_time = VALUES (update_time), nex = nex+1"
        return self.batchAdd(sql=sql, data_info=data_info)

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
        book = {}
        for key, value in xpath.items():
            book[key] = html.xpath(value)
        return book

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

    def get_book_catalog_data_list(self, book_id):
        list_tup = self._mysql_.get_book_catalog_data_list_tup(book_id)
        return list_tup

    def get_book_catalog_txt_data_list(self, book_id):
        list_tup = self._mysql_.get_book_catalog_txt_data_list_tup(book_id)
        return list_tup

    def get_book_catalog_txt_id(self, catalog_id):
        id_tup = self._mysql_.get_book_catalog_txt_id_tup(catalog_id)
        if len(id_tup) > 0:
            return id_tup[0][0]
        else:
            return 0


class Spider(Novel):
    # 1、创建小说列表页链接
    def creat_book_page_url(self):
        pass

    def creat_book_page_url_list(self):
        pass

    # 2、访问小说列表页 拿到小说列表
    def get_book_list(self, url):
        html_list = []
        flip_flag = True
        i = 1
        while flip_flag:
            print(
                '├  请求书籍列表：【 %s 】  请求 ' % (str(url)))
            time.sleep(1)
            try:
                response = requests.get(url=url)
                xml = etree.HTML(response.text)  # 整理成xml文档对象
                html_list = xml.xpath('//ul[@class="all-img-list cf"]//li')
                flip_flag = False
            except:
                print("├  请求书籍列表：【 %s 】  请求  ==》 失败 ==>  10 秒后再试" % (str(url)))
                i += 1
                time.sleep(10)
                if i > 30:
                    self._r_.setListData(name='get_book_list', lists=[str(url)])
                    flip_flag = False

        return html_list

    # 3、小说列表数据处理 格式化 book_id、src、title、img_url、state、author、chan_name、sub_name、gender、synoptic、platform、platform_src、
    def format_book_list_data(self, book_list_html, xpath):
        book_info_list = []
        for html in book_list_html:
            # print(html)
            book = self.analysis_html(html=html, xpath=xpath)
            for book_id, src, title, img_url, state, author, chan_name, sub_name, synoptic in zip(*book.values()):
                # book_id、src、title、img_url、state、author、chan_name、sub_name、gender、synoptic、platform、platform_src、
                book_info_list.append({
                    'book_id': book_id,
                    'src': src,
                    'title': title,
                    'img_url': img_url,
                    'state': state,
                    'author': author,
                    'chan_name': chan_name,
                    'sub_name': sub_name,
                    'gender': gender,
                    'synoptic': synoptic,
                    'platform': platform,
                    'platform_src': platform_src
                })
        return book_info_list

    def save_book(self, book_info_list):
        data_info = []
        for item in book_info_list:
            if item['id'] > 0 and isRepeat == False:
                print('├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】 已抓取 ==> 跳过' % (
                    item['title'], item['id'], item['book_id']))
                continue

            data_info.append((
                item['id'],
                item['book_id'],
                item['src'],
                item['title'],
                item['img_url'],
                item['state'],
                item['author'],
                item['chan_name'],
                item['sub_name'],
                item['chapter_total_cnt'],
                item['gender'],
                item['synoptic'],
                item['platform'],
                item['platform_src']))
            print('├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】 存储' % (
                item['title'], item['id'], item['book_id']))

        save_book_res = self._mysql_.save_book_info_to_mysql(data_info=data_info)
        if save_book_res == True:
            print('├  书籍信息 书籍存储 ==> 成功( %s )' % len(data_info))
            return

        print('├  书籍信息 书籍存储 ==> 失败( %s )' % len(data_info))
        self._r_.setListData(name='book_info_list', lists=[str(data_info)])

    # 4、通过 小说 book_id 拿到 小说章节列表
    def request_api_data(self, request_url):
        category_data = {}
        flip_flag = True
        i = 1
        while flip_flag:
            print("├  API ：【 %s 】 请求" % (request_url))
            try:
                response = requests.get(url=request_url)
                response.encoding = "utr-8"
                category = json.loads(response.text)
                category_data = category['data']
                flip_flag = False
            except:
                print("├  API ：【 %s 】 请求 ==》 失败 ==>  10 秒后再试" % (request_url))
                i += 1
                time.sleep(10)
                if i > 30:
                    self._r_.setListData(name='request_api_data', lists=[str(requests_url)])
                    flip_flag = False

        return category_data

    def get_book_catalog_list(self, book_list):
        book_info_list = []
        for item in book_list:
            params = {
                "_csrfToken": '',
                "bookId": item['book_id']
            }
            request_url = platform_src + "/ajax/book/category?/job_detail/?" + urlencode(params)
            catalog_info_list = self.request_api_data(request_url=request_url)
            item['catalog_list'] = self.format_book_catalog_list_data(catalog_list=catalog_info_list['vs'])
            item['chapter_total_cnt'] = catalog_info_list['chapterTotalCnt']
            book_info_list.append(item)
        return book_info_list

    # 5、小说章节列表 格式化  catalog_id、title、src、book_id、book_title、cnt、uuid、vs、vn、nex、update_time
    def format_book_catalog_list_data(self, catalog_list):
        info_list = []
        for i in catalog_list:
            for j in i['cs']:
                info_list.append({
                    'vs': i['vS'],
                    'vn': i['vN'],
                    'title': j['cN'],
                    'src': j['cU'],
                    'cnt': j['cnt'],
                    'update_time': j['uT'],
                    'uuid': j['uuid'],
                    'catalog_id': j['id']
                })
        return info_list

    def format_book_catalog_data(self, book_info):
        data_info = []
        for catalog_info in book_info['catalog_list']:
            if catalog_info['id'] > 0 and isRepeat == False:
                print(
                    '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】| 章节 【 %s 】| id 【 %s 】 | catalog_id 【 %s 】  已抓取 ==> 跳过' % (
                        book_info['title'], book_info['id'], book_info['book_id'], catalog_info['title'],
                        catalog_info['id'],
                        catalog_info['catalog_id']))
                continue

            data_info.append((
                catalog_info['id'], catalog_info['catalog_id'], catalog_info['title'], catalog_info['src'],
                book_info['id'], book_info['title'], catalog_info['cnt'], catalog_info['uuid'],
                catalog_info['vs'], catalog_info['vn'], catalog_info['update_time']
            ))
            print(
                '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】| 章节 【 %s 】| id 【 %s 】 | catalog_id 【 %s 】  存储' % (
                    book_info['title'], book_info['id'], book_info['book_id'], catalog_info['title'],
                    catalog_info['id'],
                    catalog_info['catalog_id']))
        return data_info

    def save_book_catalog(self, book_info_list):
        for item in book_info_list:
            catalog_info_list = self.format_book_catalog_data(book_info=item)
            save_catalog_res = self._mysql_.save_book_catalog_to_mysql(data_info=catalog_info_list)
            if save_catalog_res == False:
                print('├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】 | chapter_total_cnt 【 %s 】 目录存储  ==>  失败( %s )' % (
                    item['title'], item['id'], item['book_id'], item['chapter_total_cnt'], len(catalog_info_list)))
                for catalog_info in catalog_info_list:
                    save_res = self._mysql_.save_book_catalog_to_mysql(data_info=[catalog_info])
                    if save_res == False:
                        print(
                            '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】 | chapter_total_cnt 【 %s 】|  catalog_info 【 %s 】  目录存储  ==>  失败' % (
                                item['title'], item['id'], item['book_id'], item['chapter_total_cnt'],
                                str(catalog_info)))
                        self._r_.setListData(name='save_book_catalog', lists=[str(catalog_info)])
                        continue
                    print(
                        '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】 | chapter_total_cnt 【 %s 】|  catalog_info 【 %s 】  目录存储  ==>  成功' % (
                            item['title'], item['id'], item['book_id'], item['chapter_total_cnt'],
                            str(catalog_info)))
                return

            print(
                '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】 | chapter_total_cnt 【 %s 】 目录存储  ==>  成功( %s )' % (
                    item['title'], item['id'], item['book_id'], item['chapter_total_cnt'], len(catalog_info_list)))

    def update_book_id_and_catalog(self, info_list):
        book_info_list = []
        for item in info_list:
            catalog_list = []
            item['id'] = self.get_book_id(book_id=item['book_id'], platform=item['platform'],
                                          platform_src=item['platform_src'])
            catalog_id_list = self.get_book_catalog_data_list(book_id=item['id'])
            txt_id_list = self.get_book_catalog_txt_data_list(book_id=item['id'])
            for catalog_info in item['catalog_list']:
                catalog_info['id'] = self.from_list_get_id(catalog_id_list, catalog_info['catalog_id'])
                catalog_info['txt_id'] = self.from_list_get_id(txt_id_list, catalog_info['id'])
                catalog_list.append(catalog_info)

            item['catalog_list'] = catalog_list
            book_info_list.append(item)
        print('├  update_book_id_and_catalog ==> 成功')
        return book_info_list

    def from_list_get_id(self, id_list, id):
        nid = 0
        if (len(id_list)) <= 0:
            return nid
        for item in id_list:
            if id in item:
                # print(item, catalog_id)
                nid = item[0]
        return nid

    # 6、通过 小说章节 src 拿到 小说文章内容
    def get_book_txt(self, catalog_id, catalog_title, book_id, book_title, catalog_src):
        article = ''
        flip_flag = True
        i = 1
        while flip_flag:
            print(
                '├  书籍 【 %s 】| id 【 %s 】 | 章节 【 %s 】| id 【 %s 】 | catalog_src 【 %s 】  请求 ' % (
                    book_title, book_id, catalog_title, catalog_id, catalog_src))
            try:
                response = requests.get(catalog_src)
                xml = etree.HTML(response.text)
                article = u"\n".join(xml.xpath('//div[@class="read-content j_readContent"]//p/text()'))
                article = article.replace("'", "’")
                flip_flag = False
            except:
                print("├  书籍 【 %s 】| id 【 %s 】 | 章节 【 %s 】| id 【 %s 】 | catalog_src 【 %s 】  请求  ==》 失败 ==>  10 秒后再试" % (
                    book_title, book_id, catalog_title, catalog_id, catalog_src))
                i += 1
                time.sleep(10)
                if i > 30:
                    self._r_.setListData(name='get_book_txt', lists=[str(catalog_src)])
                    flip_flag = False

        return article

    def get_book_txt_list(self, book_info_list):
        data_info = []
        for item in book_info_list:
            for catalog_info in item['catalog_list']:
                if catalog_info['txt_id'] > 0 and isRepeat == False:
                    print(
                        '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】| 章节 【 %s 】| id 【 %s 】 | catalog_id 【 %s 】 | vs 【 %s 】 | txt_id 【 %s 】  已抓取 ==> 跳过' % (
                            item['title'], item['id'], item['book_id'], catalog_info['title'],
                            catalog_info['id'],
                            catalog_info['catalog_id'], catalog_info['vs'], catalog_info['txt_id']))
                    continue

                if catalog_info['vs'] == 1 and isVs == False:
                    print(
                        '├  书籍 【 %s 】| id 【 %s 】 | book_id 【 %s 】| 章节 【 %s 】| id 【 %s 】 | catalog_id 【 %s 】 | vs 【 %s 】 | txt_id 【 %s 】  会员章节 ==> 跳过' % (
                            item['title'], item['id'], item['book_id'], catalog_info['title'],
                            catalog_info['id'],
                            catalog_info['catalog_id'], catalog_info['vs'], catalog_info['txt_id']))
                    continue

                catalog_src = "https://read.qidian.com/chapter/" + catalog_info['src']
                if catalog_info['vs'] == 1:
                    catalog_src = "https://read.qidian.com/chapter/" + str(item['book_id']) + '/' + str(
                        catalog_info['catalog_id'])
                catalog_info['article'] = self.get_book_txt(catalog_id=catalog_info['id'],
                                                            catalog_title=catalog_info['title'], book_id=item['id'],
                                                            book_title=item['title'], catalog_src=catalog_src)
                data_info.append((
                    catalog_info['txt_id'],
                    catalog_info['id'],
                    catalog_info['title'],
                    item['id'],
                    item['title'],
                    catalog_info['article']
                ))
        return data_info

    # 7、小说文章内容列表数据 格式化 catalog_id、catalog_title、article
    def save_book_catalog_txt(self, book_catalog_txt_list):
        res = self._mysql_.save_book_catalog_txt_to_mysql(data_info=book_catalog_txt_list)
        if res == False:
            print('├  内容 目录存储  ==>  失败( %s )' % (len(book_catalog_txt_list)))
            for item in book_catalog_txt_list:
                save_res = self._mysql_.save_book_catalog_txt_to_mysql(data_info=[item])
                if save_res == False:
                    print('├  内容 %s 存储  ==>  失败' % (str(item)))
                    self._r_.setListData(name='save_book_catalog_txt', lists=[str(item)])
                    continue
                print('\t├  内容 %s 存储  ==>  成功' % (str(item)))
            return
        print('├  内容 存储  ==>  成功( %s )' % (len(book_catalog_txt_list)))


class SpiderModel(Spider):
    # 8、处理模式 1 一条龙（创建小说列表页链接->小说->存储小说->章节->存储章节->内容->存储内容->翻页->小说）
    def run_a_dragon(self, url, xpath):
        start = time.time()
        # 1. 请求页面 获取数据
        html_list = self.get_book_list(url=url)
        if len(html_list) <= 0:
            time.sleep(10)
            print('├  [DEBUG INFO]: 页面数据没有拿到。。。')
            self._r_.setListData(name='book_page_list', lists=[str(url)])
            return
        # 2. 格式化书籍信息
        book_list = self.format_book_list_data(book_list_html=html_list, xpath=xpath)
        book_info_list = self.get_book_catalog_list(book_list=book_list)
        # 4. 请求 目录API
        book_info_list_1 = self.update_book_id_and_catalog(info_list=book_info_list)
        # # 3. 书籍信息 存入mysql book 表
        self.save_book(book_info_list=book_info_list_1)
        book_info_list_2 = self.update_book_id_and_catalog(info_list=book_info_list_1)
        # # 6. 目录信息 存入mysql catalogs表 ，拿到id,catalog_id,src
        self.save_book_catalog(book_info_list=book_info_list_2)
        # # 7. 抓取文章内容
        book_info_list_3 = self.update_book_id_and_catalog(info_list=book_info_list_2)
        # 8. 格式化文章内容
        book_catalog_txt_list = self.get_book_txt_list(book_info_list=book_info_list_3)
        # 9. 文章内容存入 mysql txt表
        self.save_book_catalog_txt(book_catalog_txt_list=book_catalog_txt_list)
        end = time.time()
        print('├  消耗时间     ：%s 秒' % (int(float(end) - float(start))))
        print('├  抓取频率过快 180 秒后继续')
        time.sleep(180)

    # 8、处理模式 2.1 翻页抓取小说列表，保存目录到redis（创建小说列表页链接->小说->存储小说->章节->存储章节->章节列表存储到redis->翻页->小说）
    def run_save_catalog_list_to_redis(self):
        pass

    # 8、处理模式 2.2 从redis 拿到目录数据,抓取章节内容文章（从redis获取章节数据->内容->存储内容->从redis获取章节数据）
    def run_from_redis_get_catalog_save_txt_to_redis(self):
        pass

    # 8、处理模式 3.1 创建小说列表页链接,存入redis（创建小说列表页链接->存储到redis）
    def run_creat_book_page_url_list_to_redis(self):
        pass

    # 8、处理模式 3.2 从redis 拿到小说列表页链接抓取小说列表，保存目录到redis（redis列表链接->小说->存储小说->章节->存储章节->章节列表存储到redis->redis列表链接）
    def run_from_redis_get_book_list_url_save_catalog_list_to_redis(self):
        pass


class Run(SpiderModel):
    def a_dragon(self, url, xpath):
        requests_url = url
        # 1、获取url
        self.run_a_dragon(url=requests_url, xpath=xpath)
        # 2. 翻页
        pass


if __name__ == '__main__':
    gender = 1  # 性别 1:男 2: 女
    platform = "起点中文网"
    platform_src = "https://www.qidian.com"
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
        'saveBookCatalogInfoType': 'mysql',  # mysql redis
        'requests_url': [
            'https://www.qidian.com/all',
            'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1000'
        ],
        'spiderType': 1
    }
    isRepeat = False
    isVs = False
    run = Run()

    # dev  online
    environment = 'dev'

    xpath = config['xpath']
    requests_url = config['requests_url']
    for url in requests_url:
        run.a_dragon(url=url, xpath=xpath)
