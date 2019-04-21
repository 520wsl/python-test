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


# 1、创建小说列表页链接

# 2、访问小说列表页 拿到小说列表

# 3、小说列表数据处理 格式化  book_Id、src、title、img_url、state、author、chan_name、sub_name、gender、synoptic、platform、platform_src、

# 4、通过 小说 book_Id 拿到 小说章节列表

# 5、小说章节列表 格式化  catalog_id、title、src、book_Id、book_title、cnt、uuid、vs、vn、nex、update_time

# 6、通过 小说章节 src 拿到 小说文章内容

# 7、小说文章内容列表数据 格式化 catalog_id、catalog_title、article

# 8、处理模式 1 一条龙（创建小说列表页链接->小说->存储小说->章节->存储章节->内容->存储内容->翻页->小说）
# 8、处理模式 2.1 翻页抓取小说列表，保存目录到redis（创建小说列表页链接->小说->存储小说->章节->存储章节->章节列表存储到redis->翻页->小说）
# 8、处理模式 2.2 从redis 拿到目录数据,抓取章节内容文章（从redis获取章节数据->内容->存储内容->从redis获取章节数据）
# 8、处理模式 3.1 创建小说列表页链接,存入redis（创建小说列表页链接->存储到redis）