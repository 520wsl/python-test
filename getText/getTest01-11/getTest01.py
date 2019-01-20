#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/8'
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

import requests
from bs4 import BeautifulSoup
import re
import threading
import time


def directory(url):
    link = "http://www.8wenku.com"
    links = []
    r = requests.get(url)
    r.encoding = "utr-8"
    bsObj = BeautifulSoup(r.text, "lxml")
    title = bsObj.find('h2')
    print(title.get_text())
    lis = bsObj.findAll('li', {'class': "vip"})

    for i in lis:
        url = link + i.a['href']
        links.append((url, i.get_text()))
    return links


def section_load(links):
    for i in links:
        # print(i[0])

        heads = {}
        heads['Accept'] = 'application / json, text / javascript, * / *; q = 0.01'
        heads['Accept - Encoding'] = 'gzip, deflate, br'
        heads['Accept - Language'] = 'zh-CN,zh;q=0.9'
        heads['Host'] = 'www.xs8.cn'
        heads['Referer'] = 'https: // www.xs8.cn / chapter / 12284740304591203 / 32976681908229821'
        heads['User - Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        heads['X - Requested - With'] = 'XMLHttpRequest'

        r = requests.get(i[0], headers=heads)
        r.encoding = "utr-8"

        bsObj = BeautifulSoup(r.text, "lxml").find('div', {'class': 'article-body'})
        # print(str(bsObj))
        content = re.compile(r"为你一网打尽！<br/><br/>([\s\S]*?)本文来自 轻小说文库").search(str(bsObj))
        content = re.compile(r"<br/>").sub("\n", content.group(1))
        # content = re.compile(r"<p>(.*)</p>").search(content)
        return content


# links = directory("http://www.8wenku.com/book/1499")
# print(txt)
# print(links)
contents = section_load([('http://www.8wenku.com/chapter/view?id=1499&chapter_no=2', '\n序\n')])
print(contents)
