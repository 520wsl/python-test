#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
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
from aip import AipSpeech

app_id = '14975947'
api_key = "X9f3qewZCohppMHxlunznUbi"
sercret_key = "LupWgIIFzZ9kTVNZSH5G0guNGZIqqTom"

client = AipSpeech(app_id, api_key, sercret_key)
client.synthesis("沙发沙发", "zh", 1, {
    "vol": 9,
    "spd": 6,
    ""})
