from wsgiref.simple_server import make_server
from jinja2 import Template
import pymysql


def get_limit(num=1, size=10):
    start = 0
    end = int(size)
    if int(num) > 1:
        start = int(num) * int(size)
    return (start, end)


def index(params):
    with open("index2.html", "r", encoding='utf-8') as f:
        data = f.read()
    params = params.split('&')
    print(params)
    pageNum = 1
    pageSize = 10
    for param in params:
        if 'pageNum' in param:
            pageNum = param.split('=')[-1]
        elif 'pageSize' in param:
            pageSize = param.split('=')[-1]

    # print(pageNum)
    # print(pageSize)
    start_num, end_num = get_limit(num=pageNum, size=pageSize)
    print(start_num)
    print(end_num)
    template = Template(data)  # 生成模板文件
    conn = pymysql.connect(
        host='172.30.34.155',
        port=3306,
        user='root',
        password='123456',
        database='novel_online',
        charset='utf8'
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(
        'select id,title,img_url,state,author,chan_name,sub_name,synoptic,platform from book limit {0},{1};'.format(
            start_num, end_num))
    book_list = cursor.fetchall()
    if not book_list:
        book_list = []
    cursor2 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor2.execute(
        'select count(id) as count from book;'.format(
            start_num, end_num))
    book_count = cursor2.fetchone()
    ret = template.render(
        {"book_list": book_list, 'page_num': pageNum, 'page_size': pageSize, 'book_count': book_count['count']})  # 把数据填充到模板里面
    return [bytes(ret, encoding="utf8"), ]


def home(params):
    # with open("home.html", "rb") as f:
    #     data = f.read()
    # return [data, ]
    conn = pymysql.connect(
        host='172.30.34.155',
        port=3306,
        user='root',
        password='123456',
        database='novel_online',
        charset='utf8'
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    start_num = 0
    end_num = 100
    cursor.execute(
        'select id,title,img_url,state,author,chan_name,sub_name,synoptic,platform from book limit {0},{1};'.format(
            start_num, end_num))
    book_list = cursor.fetchall()
    return [bytes(str(book_list), encoding="utf8"), ]


# 定义一个url和函数的对应关系
URL_LIST = [
    ("/index/", index),
    ("/home/", home),
]


def run_server(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])  # 设置HTTP响应的状态码和头信息
    url = environ['PATH_INFO']  # 取到用户输入的url
    params = environ['QUERY_STRING']
    func = None  # 将要执行的函数
    for i in URL_LIST:
        if i[0] == url:
            func = i[1]  # 去之前定义好的url列表里找url应该执行的函数
            break
    if func:  # 如果能找到要执行的函数
        return func(params)  # 返回函数的执行结果
    else:
        return [bytes("404没有该页面", encoding="utf8"), ]


if __name__ == '__main__':
    httpd = make_server('172.30.34.114', 8008, run_server)
    print("Serving HTTP on port 8008...")
    httpd.serve_forever()
