#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '用TestCase类测试多函数多用例'
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
import unittest


def showMsg(msg):
    return "%s" % msg


def do_divide(a, b):
    return (a / b)


def ShowTrue(flag):
    return (flag)


class TestSomeFunc(unittest.TestCase):
    def testrun(self):
        self.assertEqual('OK', showMsg('OK'))
        self.assertNotEqual('OK', showMsg('NO'))
        self.assertTrue(do_divide(1, 2))
        self.assertIs(ShowTrue(False), False)
        # self.assertIs(int(do_divide(1, 2)), 1)


if __name__ == '__main__':
    unittest.main()
