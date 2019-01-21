#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/20'
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

import redis
pool=redis.ConnectionPool(host='192.168.2.202',
                          port=6379,db=8)
r=redis.StrictRedis(connection_pool=pool)
p=r.pubsub()
p.subscribe("getBookCatalog","cctv1")
for item in p.listen():
    print("Listen on channel : %s "%item['channel'].decode())
    if item['type']=='message':
        data=item['data'].decode()
        print("From %s get message : %s"%(item['channel'].decode(),item['data'].decode()))
        if item['data']=='over1':
            print(item['channel'].decode(),'停止发布')
            break
p.unsubscribe('spub')