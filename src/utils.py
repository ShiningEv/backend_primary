#coding: utf-8
import time
import os.path as osp
from jinja2 import Environment, FileSystemLoader


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open("log", 'a', encoding="utf-8") as f:
        print(dt, *args, file=f, **kwargs)


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def renderer(name, **kwargs):
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    # __file__ 就是本文件的名字
    # 得到用于加载模板的目录
    path = osp.join(osp.dirname(__file__), "templates")
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    env = Environment(loader=loader)
    t = env.get_template(name)
    return t.render(**kwargs)


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def http_response(body, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
    	h.update(headers)
    header = response_with_headers(h)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    """
    301是永久重定向，浏览器会记住，不再会访问这个网页
    302是暂时重定向
    HTTP/1.1 302 xxx
    Location: /
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')

