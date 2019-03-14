#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '队列线程案例'
__author__ = 'Mad Dragon'
__mtime__ = '2019/3/13'
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
import queue
import threading
import time
import random

q_data = queue.Queue(10)
do_thread_num = 5


def getOne(one, j):
    time.sleep(random.random() * 3)
    print('线程序号%d,获取元素%d\n' % (j, one))


class MyThread(threading.Thread):
    def __init__(self, func, data, j):
        threading.Thread.__init__(self)
        self.data = data
        self.j = j
        self.func = func

    def run(self):
        while self.data.qsize() > 0:
            self.func(self.data.get(), self.j)


if __name__ == "__main__":
    for data in range(do_thread_num * 2):
        q_data.put(data)
    for j in range(do_thread_num ):
        t1 = MyThread(getOne, q_data, j).start()
