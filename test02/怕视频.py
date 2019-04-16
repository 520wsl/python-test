#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/4/16'
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
import os
import re
import requests
from lxml import etree
from urllib import request

# 获取
url = "https://www.pearvideo.com/category_6"

headers = {
    "urser-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

resp = requests.get(url, headers=headers)
html = resp.text

# 提取
content = etree.HTML(html)
video_id = content.xpath('//div[@class="vervideo-bd"]/a/@href')
for video_addr in video_id:
    video_addr = "https://www.pearvideo.com/" + video_addr
    video_html = requests.get(video_addr).text
    reg = 'ldUrl="",srcUrl="(.*?)",vdoUrl'
    playurl = re.findall(reg,video_html)
    name = re.findall('<h1 class="video-tt">(.*?)</h1>',video_html)
    print("下载中。。。。%s"%name[0])
    path = "video"
    if path not in os.listdir():
        os.mkdir(path)
    fillname = name[0]
    request.urlretrieve(playurl[0],path+'/%s.mp4'%fillname)