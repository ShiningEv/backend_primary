'''
总结：

1 字典可以直接采用 d.get("key", "error message or function.")

2 html页面中的{{message}}可以在服务器端 body = body.replace('{{messages}}', msgs)

3 可以在__init__.py中创建基类，有许多classmethod，其他所有的类继承基类，直接调用类方法；

4 __repr__魔法函数，调用str(obj)时，实际调用__str__函数，没有时则调用__repr__

5 类的玩法多姿多彩

套路
self.__class__.__name__  返回类名
self.__dict__.items()
self, cls
cls.__name__
'''
