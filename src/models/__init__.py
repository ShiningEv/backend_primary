import json
"""
json 是一种时下非常流行的数据格式
在 python 中可以方便地使用 json 格式序列化/反序列化字典或者列表
"""

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化(上课会讲这两个名词) list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    # 序列化！！！
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        # 反序列化！！！
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)    # __init__就相当于models包，所以db就相当于同级目录！！！
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        log("models: ", models)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def find_by(cls, **kwargs):
        # u = User.find_by(username='gua')
        # kwargs = {'username': 'gua'}
        # kwargs是只有一个元素的字典...如何解析还真想了一会...有时候程序就是没有那么好看
        key, value = '', ''
        for k, v in kwargs.items():
            key, value = k, v
        models = cls.all() # all既可以被self调用，也可以被cls调用
        for model in models:
            if model.__dict__.get(key) == value:
                return model


    def __repr__(self):
        """
        这是一个 魔法函数
        不明白就看书或者 搜
        当你调用 str(o) 的时候
        实际上调用了 o.__str__()
        当没有 __str__ 的时候
        就调用 __repr__
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        # < Message\nauthor: (1dhjhjh)\nmessage: (1) >
        return '< {}\n{} >\n'.format(classname, s)


# 以下两个类用于实际的数据处理 (User / Message)
# 因为继承了 Model
# 所以可以直接 save load

# 每个文件拆的七零八落，变得简单
# 时刻考虑如何把程序变得简单！！！


if __name__ == '__main__':
    main()