#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '用字典实现 钓鱼记录'
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/3'
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

d_date1 = {'鲫鱼': [18, 10.5], '鲤鱼': [8, 6.2], '鲢鱼': [7, 4.7]}
d_date2 = {'草鱼': [2, 7.2], '鲫鱼': [3, 12], '黑鱼': [6, 15]}
d_date3 = {'乌龟': [1, 71], '鲫鱼': [1, 9.8], '草鱼': [5, 7.2], '黄鱼': [2, 40]}

fish_records = {
    '1 月 1 日': d_date1,
    '1 月 2 日': d_date2,
    '1 月 3 日': d_date3
}

nums = 0
amount = 0
day = ''
day_record = []

for day, day_record in fish_records.items():
    print('%s 钓鱼记录为：' % day)

    for name, sub_recods in day_record.items():
        nums += sub_recods[0]
        amount += sub_recods[0] * sub_recods[1]

        print('%s 数量 %d，单价 %2.f 元' % (name, sub_recods[0], sub_recods[1]))

print('钓鱼总数量为%d, 总金额为 %.2f 元' % (nums, amount))
