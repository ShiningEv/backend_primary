"""
cookie 是什么
	为什么会有cookie？
	每个浏览器发送的请求都是一样的，而服务器并不知道每一个用户是谁
	http是一个纯文本的协议，并不保持连接
	于是就在发送请求的时候加上cookie相当于邮戳，服务器就能够辨识每一个用户
	cookie都是服务器设置的
	发送响应的时候Set-Cookie字段，接受请求的时候Cookie字段
客户端和服务器怎么实现 cookie
Cookie的问题：
	Cookie可以解决身份认证，但是解决不了身份伪造，任何人都可以在HTTP请求中加入Cookie字段
	如何解决？通过Session

Cookie： user=8afgsk4s23ejj2ie
Set-Cookie： user=flfadbkjklcesd8d
...
每一次发送请求的时候，服务器都会的Set-Cookie字段都会发送新的Cookie
而浏览器也会更新Cookie存储

“为了显示此页面，Firefox 必须发送将重复此前动作的数据（例如搜索或者下订单）”
并不是浏览器与服务器交互的所有页面都会影响浏览器的Cookie存储，改变浏览器的Cookie需要响应头中有Set-Cookie字段
一般来说，只有与登录页面的交互才会刷新服务器中的Session（字典）的值 & 修改浏览器的Cookie
浏览器一旦存储了Cookie，那么发送至相同host的请求都会在request head中加上Cookie字段
这就是为什么一旦登录了一个网站，其他页面也可以登录的原因，这是浏览器会处理加上的

Session共享，则是解决了一个网站多个页面均需要验证Cookie的问题，那么设置一台甚至多台Session服务器，用于Cookie验证

Cookie很容易被劫持（劫持随机字符串伪造访问），任何一个路由器环节都可能
所以凭借Cookie可以浏览网页、看新闻等等，但一定不会仅凭Cookie就能改密码！

ARP欺骗，在公共wifi中，有坏人冒充网关，所有的数据都从假冒网关走，数据就泄漏了！

如何解决安全问题？
HTTPS，所有的请求 & 响应都是加密的，而且无法破解，数学保证！

session 是什么
	！！！在服务器端保存的用户数据！！！
	可以看到，此处Session是服务器上面存储的一个字典！保存了令牌和用户信息

session 有什么用
客户端和服务器怎么实现 session
	通过Cookie来实现
session 持久化（持久化就是重启后仍然可以使用）的两种方式
    保存到文件
    对称加密
session 共享


如何调试代码
    1，确定错误的根源，写一点测一点，写几行测几行，确保及早发现问题
    2，用 二分法 来查找问题的根源
    3，用 log 来查看代码是否被执行
    4，用 log 来查看变量的值是否是我们期待的值

作业中 model 类的新增方法实现
如何管理重复的数据
如何查找数据
"""


"""
POST /login?id=2 HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Content-Length: 25
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Cookie: Pycharm-7367d7d5=bf094603-b9e9-4994-9ebd-564f1f5ad2c0

username=gua&password=123
"""

"""
2017/02/22 19:42:48 login 的响应
HTTP/1.1 210 VERY OK
Content-Type: text/html
Set-Cookie: user=gua1

<html>
"""

"""
2017/02/22 19:45:16 ip and request, ('127.0.0.1', 50317)
GET /login HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Cookie: user=gua1
"""