#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '狂龍列表记账'
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
nums = 0
amount = 0
i = 0
fish_records = [
    '1月1日', '鲫鱼', 18, 10.5,
    '1月1日', '鲤鱼', 8, 6.2,
    '1月1日', '鲢鱼', 7, 4.7,
    '1月2日', '草鱼', 2, 7.2,
    '1月2日', '鲫鱼', 3, 12,
    '1月2日', '黑鱼', 6, 15,
    '1月3日', '乌龟', 1, 71,
    '1月3日', '鲫鱼', 1, 9.8
]

print('钓鱼日期 名称 数量 单价(元)')
print('-' * 40)

while i < len(fish_records):
    nums = nums + fish_records[i + 2]
    amount = amount + fish_records[i + 2] * fish_records[i + 3]

    print('%s, %s, %.2f, %d' % (fish_records[i], fish_records[i + 1], fish_records[i + 2], fish_records[i + 3]))
    i = i + 4
print('-'*40)

print('总数%d， 总金额%.2f 元'%(nums,amount))