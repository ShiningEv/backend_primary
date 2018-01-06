# coding: utf-8

"""
url 的规范
protocol://host:port/address?query
第一个 ? 之前的是 path
? 之后的是 query
http://c.cc/search?a=b&c=d&e=1
PATH  /search
QUERY a=b&c=d&e=1
"""

import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict
# 注意要用 from import as 来避免重名
from routes_todo import route_dict as todo_route


# 定义一个 class 用于保存请求的数据
class Request(object):

    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.headers = {}
        self.body = ''
        self.cookies = {}

    def add_cookies(self):
        """
        height=169; user=gua
        :return:
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        [
            'Accept-Language: zh-CN,zh;q=0.8'
            'Cookie: height=169; user=gua'
        ]
        """
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.cookies = {}
        self.add_cookies()

    # 这里的body是request中请求的body
    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # Content-Type: application/x-www-form-urlencoded
        # URL encoded
        # 以上的编码格式会将空格、&、？等特殊符号转换为%26、%3F等等...
        # 因为url中能够使用的字符是有规定的，不能使用空格等...
        # 而实际上解析的时候，需要将拿到转码后的数据转回去，采用urllib.parse.unquote函数

        # username=g+u%26a%3F&password=
        # username=g u&a?&password=
        # TODO, 这实际上算是一个 bug，应该在解析出数据后再去 unquote

        # 学习的时候要抓住主要矛盾，去理解程序的意图和设计思想，不要深陷在无谓的细节之中！！！
        # 主要矛盾！理论学习不要陷入细节
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    # parsed_path 用于把 path 和 query 分离
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """

    # 图片,js,css文件等都是静态文件
    # 是在html中遇到后需要发送请求的文件！！！
    # 譬如<img src="/static?file=doge.gif"/>中的src就需要发一个http request请求图片
    # 不可能针对每一个静态文件都写一个静态路由
    # 所以希望采用route_static统一处理对静态文件的路由请求！传入文件名即可返回相应文件
    r = {
        '/static': route_static,
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    # 处理的路由越来越多，以上文件会越来越大
    # 越复杂的程序，越需要降低复杂性
    # 如何降低复杂度：让功能尽可能地隔离开，
    # 并且在完整隔离开的程序中，让每一个代码文件各司其职，互不干扰
    # 这样每一个文件几百行都能够hold住

    # update是dict的函数，用于将route_dict合并到r中
    # get也是dict的函数，传入两个参数：key & error函数
    r.update(route_dict)
    r.update(todo_route)
    response = r.get(path, error)
    return response(request)


request = Request()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            log('\n\n-------------------------new request-------------------------')
            log('original requests: \n', r)
            r = r.decode('utf-8')
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            # parse request
            # path
            path = r.split()[1]
            log("path: ", path)
            # method
            request.method = r.split()[0]
            # headers
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            # request body
            request.body = r.split('\r\n\r\n', 1)[1] # 不论如何处理，r终究是request！请求头的body！
            log("request.body: ", request.body)
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            # 把响应发送给客户端
            connection.sendall(response)
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3011,
    )
    run(**config)
