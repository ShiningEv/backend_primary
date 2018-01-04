"""
0, 改进 log 把记录写入文件


1, 模板和模板使用方法
参考下面 2 个文件
jinja_demo.py
templates/demo.html
### 用于替换之前在route函数中替换{{}}
### 完全将代码和生成页面逻辑的部分放在html中
### 全世界所有的页面都是通过模板生成的。非常重要！

### 前后端如何合作？
### 前端把页面写好，由后端写模板，往模板中塞数据

### 路由分两种：
### 第一种：像add、delete、update，纯粹接受POST请求，处理数据，发送重定向
### 第二种：像index、edit，只发送页面，不做其他事情

### 程序先直白的写出来，如果有重复代码再单独拎出来重构
### 程序中只有函数，而且每一个函数都很短

2, 用模板实现 todo 程序
参考下面 2 个文件
routes_simpletodo.py
templates/simple_todo_index.html


3, 用模板实现注册/登录
参考下面 2 个文件
routes_user.py
templates/login.html
templates/register.html


4, python package(包, 也就是高级模块)
"""
