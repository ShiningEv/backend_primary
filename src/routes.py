from utils import log
from utils import template
from utils import renderer
from utils import http_response
from utils import redirect
from models.message import Message
from models.user import User

import random


# 这个函数用来保存所有的 messages
message_list = []
# session 可以在服务器端实现过期功能
session = {}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        # 写程序简单快速写完了就好了，不要大致纠结细节
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    # username = request.cookies.get('user', '【游客】')
    return username


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    username = current_user(request)
    body = renderer('index.html', username = username)
    return http_response(body)


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {}
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            session[session_id] = u.username
            log("session: ", session)
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # 下面是把用户名存入 cookie 中
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = renderer('login.html', result=result, username=username)
    return http_response(body, headers)


def route_admin(request):
    """
    登录admin页面的路由函数
    """
    log('login, cookies', request.cookies)
    username = current_user(request)
    u = User.find_by(username=username)
    if u is None or u.role != 1:
        return redirect('/login')
    us = User.all()
    body = renderer('admin.html', users = us)
    # body = body.replace('{{result}}', "<pre>{}</pre>".format(User.all()))
    return http_response(body)


def route_admin_update(request):
    """
    用于admin页面修改密码的路由
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        form = request.form()
        user_id = int(form.get('id', -1))
        user = User.find_by(id=user_id)
        if user is None:
            result = "用户 id={} 不存在".format(3)
            return redirect('/admin/users')
        passwd = form.get('password', '')
        user.password = passwd
        if user.validate_register():
            user.save()
            # result = '密码修改成功'
        # else:
            # result = '用户名或者密码长度必须大于2'
    return redirect('/admin/users')


def route_register(request):
    """
    注册页面的路由函数
    GET，则是请求register页面
    POST，则是用户注册
    """
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2 || 已存在用户名'
    else:
        result = ''
    body = renderer('register.html', result=result)
    return http_response(body)

def route_message(request):
    """
    消息页面的路由函数
    """
    username = current_user(request)
    if username == '【游客】':
        log("**debug, route msg 未登录")
        return redirect('/')
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        msg.save()
    ms = Message.all()
    body = renderer('html_basic.html', messages = ms)
    # 这里的str(m)，m是一个对象，调用了魔法函数__repr__!!!
    # msgs = '<br>'.join([str(m) for m in message_list])
    # body = body.replace('{{messages}}', msgs)
    return http_response(body)


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path  '/static'
    query = {
        'file', 'doge.gif',
    }
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_profile(request):
    '''
    如果登录了, 则返回一个页面显示用户的三项资料(id, username, note)
    如果没登录, 返回 302 为状态码来 重定向到登录界面
    当返回 302 响应的时候, 必须在 HTTP 头部加一个 Location 字段并且设置值为你想要定向的页面
    '''
    log('profile request: ', request)
    username = current_user(request)
    u = User.find_by(username=username)
    log('find user: ', u)
    if u is not None:
        body = renderer('info.html', username=u.username, id=u.id, note=u.note)
        return http_response(body)
    else:
        return redirect("http://localhost:3000/login")


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/profile': route_profile,
    '/admin/users': route_admin,
    '/admin/user/update': route_admin_update,
}
