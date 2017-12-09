# coding: utf-8
import socket

# 这个程序就是一个套路程序, 套路程序没必要思考为什么会是这样
# 记住套路, 能用, 就够了
# 运行这个程序后, 浏览器打开 localhost:2000 就能访问了
#
# 服务器的 host 为空字符串, 表示接受任意 ip 地址的连接
# port 是端口, 这里设置为 2000, 随便选的一个数字
host = '0.0.0.0'
port = 2000

# s 是一个 socket 实例
s = socket.socket()
# s.bind 用于绑定
# 注意 bind 函数的参数是一个 tuple
s.bind((host, port))

# 用一个无限循环来处理请求
while True:
    # 套路, 先要 s.listen 开始监听
    # 注意 参数 5 的含义不必关心
    s.listen(5)
    # 当有客户端过来连接的时候, s.accept 函数就会返回 2 个值
    # 分别是 连接 和 客户端 ip 地址
    connection, address = s.accept()
    print("connection:{}, address:{}".format(connection, address))
    '''
    port of address is random:
    connection:<socket.socket fd=312, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2000), raddr=('127.0.0.1', 5517)>, 
    address:('127.0.0.1', 5517)
    connection:<socket.socket fd=312, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2000), raddr=('127.0.0.1', 5518)>, 
    address:('127.0.0.1', 5518)
    '''
    # recv 可以接收客户端发送过来的数据
    # 参数是要接收的字节数
    # 返回值是一个 bytes 类型
    request = connection.recv(1024)
    # 取完所有的数据
    # buffer_size = 1024
    # request = b''
    # while True:
    #     request_part = connection.recv(buffer_size)
    #     request += request_part.encode('utf-8')
    #     # 取到数据的长度不够recv参数的时候，说明数据已经取完了
    #     if len(request_part) < buffer_size:
    #         break

    # bytes 类型调用 decode('utf-8') 来转成一个字符串(str)
    print('ip and request, {}\n{}'.format(address, request.decode('utf-8')))
    # b'' 表示这是一个 bytes 对象
    response = b'HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>'
    # 用 sendall 发送给客户端
    connection.sendall(response)
    # 发送完毕后, 关闭本次连接
    connection.close()

'''
### example of request
GET / HTTP/1.1
Host: localhost:2000
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6,zh-TW;q=0.5
Cookie: Pycharm-5a80fe93=d8186142-2b90-4feb-827f-fdfdf4a3dfa5
'''