#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '线程测试'
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/10'
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
import time
import threading, queue

def eating(n):
    #消费
    i = q.get()
    print(i[1])
    print('消费者%d吃了第%d份食物' % (n, i[0]))


def making():
    #生产
    for i in range(1, 11):
        print('正在制作第%d份食物' % i)
        time.sleep(1)
        link = (i,'名字')
        q.put(link)


if __name__ == '__main__':
    q = queue.Queue()
    t2 = threading.Thread(target=making)
    t2.start()
    for i in range(1, 11):
        t = threading.Thread(target=eating, args=(i,))
        t.start()
