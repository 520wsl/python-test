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
    print(data)
    # 给客户端回复消息
    conn.send(b'http/1.1 200 ok \r\ncontent-type:text/html; charset=utf-8\r\n\r\n')
    # 想让浏览器在页面上显示出来的内容都是相应正文
    conn.send(b'<h1>Hello woder !</h1>')
    # 关闭
    conn.close()
    sk.close()
