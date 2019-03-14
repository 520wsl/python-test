#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '测试自定义函数'
__author__ = 'Mad Dragon'
__mtime__ = '2019/3/14'
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
import math
# from testfunction import *

def sums(*num):
    # '''
    # >>> sums(1,2,3,4,5)
    # 15
    # >>> sums(2,3,4,5)
    # 累加为： 14.000000
    # 14
    # >>> sums('q',2,3,4,5)
    # 14
    # >>> sums('a'2,3,4,5)
    # 14
    # '''
    total = math.trunc(sum(num))
    print('累加为： %f' % total)
    return total


if __name__ == '__main__':
    import doctest

    # doctest.testmod(verbose=False)
    doctest.testfile('test_content.txt', verbose=False)
