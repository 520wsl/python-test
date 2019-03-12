#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '简易组件使用案例'
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
from tkinter import *
import tkinter.messagebox

master = Tk()
class Example(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("演示鼠标右键跳出菜单")

        self.menu=Menu(self.master,tearoff=0)
        self.menu.add_command(label='提示',command=self.showClick)
        self.menu.add_command(label='退出',command=self.onExit)
        self.master.bind("<Button-3>",self.showMenu)
        self.pack()
    def showMenu(self,e):
        self.menu.post(e.x_root,e.y_root)
    def showClick(self):
        # tkinter.messagebox.showinfo("提示","鼠标点上了！")
        tkinter.messagebox.showerror("提示","鼠标点上了！")
    def onExit(self):
        self.quit()



master.geometry("700x600")

master['background'] = 'LightSlateGray'
master.iconbitmap('I:\\硬盘转移文件\\D\\upupoobin\\WallPaper\\index\\img\\favicon.ico')

master.title("恭喜你中了一百万！")
Example()
l_show = Label(master, text="三酷猫：")
# photo = PhotoImage("I:\\硬盘转移文件\\D\\upupoobin\\WallPaper\\index\\img\\favicon.ico")
# l_show1 = Label(master, image=photo)
l_show.pack(side="left")
# l_show1.pack(side="left")

e_show = Entry(master, width=10)
e_show.pack(side="left")

t_show = Text(master,width=10, height=4)
t_show.pack(side='bottom')

m1 = Menu(master)
master.config(menu=m1)
def callback():
    master.title("OK")

filemenu = Menu(m1)
m1.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label='New',command=callback)
filemenu.add_command(label='Open...',command=callback)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=callback)

helpmenu = Menu(m1)

m1.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About...',command=callback)
master.mainloop()
