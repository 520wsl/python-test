#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '窗口应用  编辑器'
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/23'
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
import wx

def load(event):
    file = open(fileName.GetValue())
    fileContent.SetValue(file.read())
    file.close()
def save(event):
    file = open(fileName.GetValue(),'w')
    file.write(fileContent.GetValue())
    file.close()

app = wx.App()
win = wx.Frame(None, title="Hello World!  ljm")
win.Show()

openButton = wx.Button(win, label="Open", pos=(225, 5), size=(80, 25))
openButton.Bind(wx.EVT_BUTTON,load)
saveButton = wx.Button(win, label="Save", pos=(315, 5), size=(80, 25))
saveButton.Bind(wx.EVT_BUTTON,save)
fileName = wx.TextCtrl(win, pos=(5, 5), size=(210, 25))
fileContent = wx.TextCtrl(win, pos=(5, 35), size=(390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
print(fileContent)

app.MainLoop()
