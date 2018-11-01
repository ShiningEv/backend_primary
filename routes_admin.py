from models  import User
from routes import current_user
from routes_todo import template
from routes_todo import response_with_headers
from routes_todo import redirect
from routes_todo import login_required


def admin(request):
    """
    admin 首页的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None or u.role != 1:
        return redirect('/login')
    user_list = User.all()
    user_html = ''.join(['<h3>id</h3>{}<h3>username</h3>{}<h3>password</h3>{}<br><br>'
                        .format(u.id, u.username, u.password) for u in user_list])
    # 替换模板文件中的标记字符串
    body = template('user_admin.html')
    body = body.replace('{{users}}', user_html)
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def update(request):
    if request.method == 'POST':
        form = request.form()
        user_id = int(form.get('id', -1))
        user = User.find_by(id=user_id)
        if user is None:
            return redirect('/login')
        user.password = form.get('password', user.password)
        user.save()
    return redirect('/admin/user')


route_dict = {
    '/admin/user': login_required(admin),
    '/admin/user/update': login_required(update),
}