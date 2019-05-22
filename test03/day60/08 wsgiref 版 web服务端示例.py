"""
根据URL中不同的路径返回不同的内容--函数进阶版
返回HTML页面
让网页动态起来
wsgiref模块版
"""

import time
from wsgiref.simple_server import make_server


# 定义一个处理 /yimi/ 的函数
def yimi(url):
    with open('yimi.html', 'r', encoding='utf-8') as f:
        ret = f.read()
    ret2 = ret.replace('@@xx@@', str(time.time()))
    return bytes(ret2, encoding='utf-8')


# 定义一个处理 /xiaohei/ 的函数
def xiaohei(url):
    with open('xiaohei.html', 'rb') as f:
        ret = f.read()
    return ret


def f404(url):
    return bytes('<h1>404 ! not  found : {} </h1>'.format(url), encoding='utf-8')


list1 = [
    ('/yimi/', yimi),
    ('/xiaohei/', xiaohei),
]


def run_server(environ, start_response):
    start_response('200 OK', [
        ('Content-Type', 'text/html;charset=utf8'),
    ])
    url = environ['PATH_INFO']
    func = None

    for i in list1:
        if i[0] == url:
            func = i[1]
            break

    if func:
        response = func(url)
    else:
        response = f404(url)

    return [response, ]


if __name__ == '__main__':
    httpd = make_server('172.30.34.114', 8008, run_server)
    print('http://172.30.34.114:8008')
    httpd.serve_forever()
