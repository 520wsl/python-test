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


class Box1:
    def __init__(self, length1, width1, height1):
        self.length = length1
        self.width = width1
        self.height = height1

    def volume(self):
        return self.length * self.width * self.height


class Box2(Box1):
    def __init__(self, length1, width1, heigth1):
        super(Box2, self).__init__(length1, width1, heigth1)
        self.color = 'white'
        self.material = 'paper'
        self.type = 'fish'

    def are(self):
        re = self.height * self.width + self.length * self.height + self.width * self.height
        return re * 2


my_box2 = Box2(10, 10, 10)
print(my_box2.volume())
print(my_box2.are())
print(my_box2.color)
print(my_box2.material)
print(my_box2.type)
