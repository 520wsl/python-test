#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '小说抓取'
__author__ = 'Mad Dragon'
__mtime__ = '2019/4/15'
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
# https://www.qidian.com/all
# 设计模式 -- 面向对象
import os

import requests
import xlwt
from lxml import etree


class Spider(object):
    def start_request(self):
        # 1. 请求一级页面拿到数据， 抽取小说名、小说链接 创建文件夹
        response = requests.get("https://www.qidian.com/all")
        xml = etree.HTML(response.text)  # 整理成xml文档对象
        Bigtit_list = xml.xpath('//div[@class="book-mid-info"]/h4/a/text()')
        Bigscr_list = xml.xpath('//div[@class="book-mid-info"]/h4/a/@href')
        for Bigtit, Bigsrc in zip(Bigtit_list, Bigscr_list):
            print(Bigtit, Bigsrc)
            if os.path.exists(Bigtit) == False:
                os.mkdir(Bigtit)
            self.next_file(Bigtit, Bigsrc)

    # 2. 请求二级页面乃刀数据， 抽取章节名、那链接
    def next_file(self, Bigtit, Bigsrc):
        print(Bigtit)
        print(Bigsrc)
        response = requests.get("http:" + Bigsrc+'#Catalog')
        xml = etree.HTML(response.text)
        print(xml.xpath('//a/text()'))
        Littit_list = xml.xpath('//ul[@class="cf"]//li/a/text()')
        Litsrc_list = xml.xpath('//ul[@class="cf"]//li/a/@href')
        print(Littit_list)
        print(Litsrc_list)
        for Littit, Litsrc in zip(Littit_list, Litsrc_list):
            print(Littit, Litsrc)
            # self.finally_file(Littit=Littit, Litsrc=Litsrc, Bigtit=Bigtit)

    # 3. 请求三级页面拿到数据， 抽取文章内容，保存数据
    def finally_file(self, Littit, Litsrc, Bigtit):
        # f = xlwt.Workbook()
        response = requests.get("http:" + Litsrc)
        # print(response)
        xml = etree.HTML(response.text)
        # print(xml)
        # print(xml.xpath('//div'))

        content = "\n".join(xml.xpath('//div[@class="read-content j_readContent"]//p/text()'))
        print(content)
        fileName = Bigtit + "\\" + Littit + ".txt"
        print("正在保存小说文件：" + fileName)
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(content)


spider = Spider()
spider.start_request()
