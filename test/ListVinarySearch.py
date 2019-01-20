#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2018/12/28'
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
fish_records = [1,1,2,3,6,7,8,18]
low = 0
high = len(fish_records) - 1
find_value = 18
find_OK = False
i = 1

while low <= high:
    middle = int((low + high) / 2)
    if find_value == fish_records[middle]:
        find_OK = True
        break
    elif find_value > fish_records[middle]:
        low = middle + 1
    elif find_value < fish_records[middle]:
        high = middle - 1
    i += 1

if find_OK:
    print('%d 在列表下标%d处，找了%d次。' % (find_value, middle, i))
else:
    print('要找的数%d没有！找了%d次。' % (find_value, i))
