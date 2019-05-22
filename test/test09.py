#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/2/21'
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
import tkinter

MainForm = tkinter.Tk()
MainForm.geometry("600x700")
MainForm['background'] = 'LightSlateGray'
# MainForm.iconbitmap('I:\\硬盘转移文件\\D\\upupoobin\\WallPaper\\index\\img\\favicon.ico')

MainForm.title("恭喜你中了一百万！")


def turn_property(event):
    event.widget['activeforeground'] = "red"
    event.widget['text'] = "OK"
def turn_property2(event):
    event.widget['activeforeground'] = "black"
    event.widget['text'] = "恭喜你中了一百万"


btn1 = tkinter.Button(MainForm, text="退出", fg="black")
btn1.bind("<Enter>", turn_property)
btn1.bind("<Leave>", turn_property2)
btn1.pack()

btn2 = tkinter.Button(MainForm, text="2", fg="black")
btn3 = tkinter.Button(MainForm, text="3", fg="black")
btn4 = tkinter.Button(MainForm, text="4", fg="black")
btn5 = tkinter.Button(MainForm, text="5", fg="black")
btn2.pack(side='left',padx="1m")
btn3.pack(side='left',padx="1m")
btn4.pack(side='left',padx="1m")
btn5.pack(side='left',padx="1m")
MainForm.mainloop()
