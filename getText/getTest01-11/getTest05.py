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


class load_book(object):
    def __init__(self, host, pageSize):
        self.b_host = host
        self.b_pageSize = pageSize
        self.b_pageCount = self.b_pageCount_load()
        # self.b_links = self.b_links_load()
        self.b_links = []
        self.content = []
        self.mysql_ip = "172.30.34.210"
        self.mysql_user = "root"
        self.mysql_pwd = "root"
        self.mysql_database = "pythonTest"
        self.errorurls = [
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=21',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=14',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=18',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=29',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=33',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=26',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=19',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=34',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=27',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=45',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=31',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=24',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=49',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=35',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=39',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=36',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=54',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=40',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=44',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=69',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=62',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=55',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=48',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=73',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=66',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=52',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=70',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=74',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=85',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=78',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=89',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=75',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=86',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=90',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=83',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=76',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=94',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=105',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=95',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=99',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=117',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=110',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=96',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=114',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=107',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=118',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=129',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=115',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=108',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=133',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=119',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=112',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=137',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=130',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=116',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=123',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=141',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=134',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=127',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=120',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=138',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=131',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=124',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=149',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=142',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=128',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=139',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=150',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=143',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=136',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=169',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=173',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=159',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=152',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=177',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=170',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=163',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=181',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=167',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=160',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=178',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=171',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=164',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=175',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=168',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=193',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=186',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=172',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=197',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=183',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=201',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=187',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=198',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=191',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=209',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=195',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=199',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=210',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=203',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=196',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=221',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=200',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=218',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=211',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=229',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=215',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=208',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=233',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=212',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=237',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=223',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=216',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=241',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=234',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=227',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=220',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=224',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=228',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=246',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=243',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=240',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=265',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=244',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=262',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=255',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=266',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=260',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=285',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=264',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=289',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=282',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=272',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=302',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=295',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=306',
            'http://www.xs8.cn/all?pageSize=500&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=300']

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
            self.b_pageSize) + '&gender=2&catId=-1&isFinish=-1&isVip=-1&size=-1&updT=-1&orderBy=0&pageNum=' + str(
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
            'User - Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        heads['X - Requested - With'] = 'XMLHttpRequest'

        try:
            r = requests.get(url, headers=heads)
            r.encoding = "utr-8"
            return r.text
        except:
            print("获取列表失败,一秒后重试，失败链接：", url)
            time.seleep(1)
            self.b_link_load()

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
        sql = "INSERT INTO `books` (`book_Id`, `book_name`, `state`, `author`, `chan_name`, `synoptic`, `img_url`) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE book_Id = VALUES(book_Id), book_name = VALUES(book_name), state = VALUES(state), author = VALUES(author), chan_name = VALUES(chan_name), synoptic = VALUES(synoptic), img_url = VALUES(img_url) "
        return self.batchAdd(sql, data_info)

    # 获取书本数据
    def getBooksInfo(self, booksData):
        booksInfo = []
        for i in booksData:
            booksInfo.append(
                (i['book_Id'], i['book_name'], i['state'], i['author'], i['chan_name'], str(i['synoptic']),
                 i['img_url']))
        return booksInfo

    # 获取 没页数据 并 存入数据库
    def item_get_and_save(self, link):
        content = self.parseWithXpath(self.getHtmlText(link))
        getBooksInfoData = self.getBooksInfo(content)
        # self.content.append(getBooksInfoData)
        print("链接 [ %s ] 抓取完成...\n" % link)
        if len(getBooksInfoData) < self.b_pageSize:
            self.errorurls.append(link)
        time.sleep(30)
        self.write_txt(getBooksInfoData)

    # 按组获取
    def section_load(self, links):
        if len(links) <= 0:
            return;

        for link in links:
            time.sleep(30)
            self.item_get_and_save(link)

    # 调度
    def contents_load(self, loops=10):
        threads = []
        nloops = range(loops)
        task_list = []
        task_size = len(self.b_links) // loops + 1
        for i in nloops:
            try:
                task_list.append(self.b_links[i * task_size:(i + 1) * task_size])
            except:
                task_list.append(self.b_links[i * task_size:])

        # print(task_list)

        for i in nloops:
            t = threading.Thread(target=self.section_load, args=([task_list[i]]))
            threads.append(t)

        # print(threads)

        for i in nloops:
            #  threads[i].setDaemon(True)
            time.sleep(30)
            threads[i].start()
        #   for j in nloops:
        #      threads[j].join()

    def write_txt(self, getBooksInfoData):
        print("开始 存储 链接类容")
        getBooksInfoRes = self.saveBooks(getBooksInfoData)
        # for i in getBooksInfoData:
        #     print('\tbookId： %s \t书名： 《%s》 \t作者： %s \t状态： %s \t分类： %s \n\t图片： %s ' % (
        #         i[0], i[1], i[3], i[2], i[4], i[6]))

        if not getBooksInfoRes:
            print('书籍信息存储失败')
        else:
            print('存储 %d 成功！' % len(getBooksInfoData))


if __name__ == '__main__':
    book = load_book('http://www.xs8.cn', 500)
    book.contents_load(100)
    print(book.errorurls)
