#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
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
d_date1 = {
    '三酷猫': {
        '鲫鱼': [17, 10.5],
        '鲤鱼': [8, 6.2],
        '鲢鱼': [7, 4.7]
    },
    '加菲猫': {
        '黑鱼': [8, 16]
    },
    '大脸猫': {
        '草鱼': [12, 8]
    }
}

d_date2 = {
    '三酷猫': {
        '草鱼': [2, 7.2],
        '鲫鱼': [3, 12],
        '黑鱼': [6, 15]
    },
    '加菲猫': {
        '鲤鱼': [9, 7.1]
    }
}

d_date3 = {
    '三酷猫': {
        '乌龟': [1, 78.10],
        '鲫鱼': [1, 10.78],
        '草鱼': [5, 7.92]
    },
    '大脸猫': {
        '鲫鱼': [8, 9.8],
        '螃蟹': [5, 15],
    }
}


fish_records = {
    '1 月 1 日': d_date1,
    '1 月 2 日': d_date2,
    '1 月 3 日': d_date3
}

nums = 0
amount = 0
day = ''

print('----------每日钓鱼记录--------------')

for day, day_record in fish_records.items():
    if nums > 0:
        print('---------------------------------------------')

    day_nums = 0
    day_amount = 0
    print('%s 钓鱼记录为：' % day)

    for name1, get_fish_record1_d in day_record.items():
        print('    %s'% name1)

        for name2, get_fish_record2_d in get_fish_record1_d.items():
            day_nums += get_fish_record2_d[0]
            day_amount += get_fish_record2_d[0] * get_fish_record2_d[1]
            print('            %s 数量 %d，单价 %.2f 元' % (name2, get_fish_record2_d[0], get_fish_record2_d[1]))

    print('%s,钓鱼数量为%d,金额为%.2f元' % (day,day_nums, day_amount))

    nums += day_nums
    amount += day_amount

print('=========统计结果打印=================')
print('钓鱼总数量为%d, 总金额为 %.2f 元' % (nums, amount))