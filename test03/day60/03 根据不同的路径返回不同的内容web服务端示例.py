import socket

# 生成 socket 实例对象
sk = socket.socket()

sk.bind(('172.30.34.114', 8008))
# 监听
sk.listen()

# 写一个死循环，一直等待客户端来连接我
while 1:
    # 获取客户端的链接
    conn, _ = sk.accept()
    # 接受客户端发来的消息
    data = conn.recv(8096)
    # print(data)
    # 把收到的数据转换成字符串类型
    data_str = str(data, encoding='utf-8')
    print(data_str)
    # 用 \r\n 去切割上面的字符串
    l1 = data_str.split('\r\n')
    print(l1[0])
    # 按照空格切割上面的字符串
    l2 = l1[0].split()
    print(l2[1])
    url = l2[1]
    # 给客户端回复消息
    conn.send(b'http/1.1 200 ok \r\ncontent-type:text/html; charset=utf-8\r\n\r\n')
    # 想让浏览器在页面上显示出来的内容都是相应正文

    # 根据不同的url返回不同的内容
    if url == '/yimi/':
        conn.send(b'<h1>Hello YIMI !</h1>')
    elif url == '/xiaohei/':
        conn.send(b'<h1>Hello XIAOHEI !</h1>')
    else:
        conn.send(b'<h1>404</h1>')


    # 关闭
    conn.close()
    sk.close()
