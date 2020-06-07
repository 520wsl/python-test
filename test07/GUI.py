import os
import threading
import time
from tkinter import *
from tkinter import ttk
from tkinter import StringVar
from tkinter.filedialog import askdirectory, askopenfilename

from PIL import ImageTk

root = Tk()
start_time = time.time()


#
# def selectDirPath():
#     path_ = askdirectory()
#     path.set(path_)
#
#
# def selectFilePath():
#     # 选择文件path_接收文件地址
#     path_ = askopenfilename()
#
#     # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
#     # 注意：\\转义后为\，所以\\\\转义后为\\
#     path_ = path_.replace("/", "\\\\")
#     # path设置path_的值
#     path.set(path_)

def print_message(txt):
    msgbox.insert(END, 'test\n')


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


def test(only_first):
    print(only_first)
    print('test')
    print_message(only_first)





if __name__ == "__main__":
    file_path = os.path.join(os.path.join('template'), 'template.xls')
    title = '百度爱采购查排名小助手-V2.0.0'
    root.title('{} 395548460@qq.com'.format(title))
    root.iconbitmap('./imgs/icon.ico')

    # logo 标题
    logo_path = os.path.join('./imgs/logo.jpg')
    photo = ImageTk.PhotoImage(file=logo_path)
    Label(root, image=photo, width=64, height=64).grid(row=0, column=0, columnspan=2, stick='e')
    Label(root, text=title, font=('Arial 14 bold'), ).grid(row=0, column=2)
    Label(root, text="查排名模式:").grid(row=1, column=0)
    inputQual = ttk.Combobox(root, state="readonly")
    inputQual['value'] = ('只查询第一个', '查询第一页')
    keyTrans = dict()
    keyTrans['只查询第一个'] = True
    keyTrans['查询第一页'] = False
    inputQual.current(0)
    inputQual.grid(row=1, column=1, columnspan=1, sticky='nse')

    Button(root, text="开始查询", command=lambda: thread_it(test, keyTrans[inputQual.get()])).grid(row=1, column=2)
    msgbox = Text(root, width=100)
    msgbox.insert('1.0',
                  "{}\n\n一、查询模式：\n\t1、只查询第一个：当关键词查询到产品后既返回结果\n\t2、查询第一页：查询当前关键词第一页所有符合要求的产品信息\n二、关键词模板：\n\t关键词模板采用/template/template.xls表格，第一列要匹配的公司名，第二列要查询的关键词\n\n".format(
                      title))
    msgbox.grid(row=2, column=0, rowspan=10, columnspan=10)

    root.geometry('900x800')
    root.mainloop()
