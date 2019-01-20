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


class Color1:
    '''求立方体的颜色'''

    def __init__(self, index=0):
        self.set_color = ['white', 'red', 'black', 'green']
        self.index = index

    def setColor(self):
        return self.set_color[self.index]


class Box1:
    '''求立方体的类'''

    def __init__(self, length1, width1, height1, c1=0):
        self.length = length1
        self.width = width1
        self.height = height1
        self.color0 = Color1(c1).setColor()

    def volume(self):
        return self.length * self.width * self.height


my_box1 = Box1(length1=10, width1=10, height1=20,c1=1)

print('立方体体积是%d' % (my_box1.volume()))

print(my_box1.length)
print(my_box1.height)

print(my_box1.volume())

print(my_box1.color0)
