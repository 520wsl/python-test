#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/5'
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


def recursion_sum(num):
    if num == 1:
        return num
    return recursion_sum(num - 1) + num


print(recursion_sum(4))


def recursion_sum2(num):
    if num == 1:
        return num

    tt = recursion_sum2(num - 1) + num
    print('第%d次递归' % num)
    print('返回值%d在内存中地址:%d' % (tt, id(tt)))
    return tt


print(recursion_sum2(10))
