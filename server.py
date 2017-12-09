# coding: utf-8

import socket

"""
0, 请注意代码的格式和规范(PEP8)
1, 规范化生成响应
2, HTTP 头
3, 几个常用 HTML 标签及其用法
4, 浏览器向服务器传递参数的两种方式
"""

'''
一个程序都只能有一个入口 if __name__ ==  '__main__'
所有的内容都应该写在函数里面
'''

def log(*args, **kwargs):
    """
    用这个 log 替代 print
    在任何语言中都不应该用原生的print，应该包裹之后再使用
    """
    print('log', *args, **kwargs)


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello Gua</h1><img src="/doge.gif">'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


def route_msg():
    """
    msg 页面的处理函数
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_json():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/json\r\n'
    body = page('json')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def error(code=404):
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


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    '''
    这里的路径叫做路由
    '''
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/msg': route_msg,
        '/json': route_json,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('raw, ', request)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里用 try 防止程序崩溃
                path = request.split()[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # 把响应发送给客户端
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            # 处理完请求, 关闭连接
            connection.close()


def main():
    # 生成配置并且运行程序
    """
    dict内容的一致性，末尾的逗号
    """
    config = dict(
        host='',
        port=3000,
    )
    run(**config)


if __name__ == '__main__':
    main()