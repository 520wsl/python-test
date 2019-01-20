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
fish_records = [18,8,7,2,3,6,1,1]
i = 0
compare = 0

fish_len = len(fish_records)

while i < fish_len:
    j = 1
    while j < fish_len -i:
        if fish_records[j-1] > fish_records[j]:
            compare = fish_records[j-1]
            fish_records[j-1] = fish_records[j]
            fish_records[j] = compare
        j+=1
    i+=1

print(fish_records)