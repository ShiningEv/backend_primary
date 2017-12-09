from models import Model

# User 和 Message可以存储各种各样的数据
# 想要存储什么样的数据，就定义一个类！

class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        all_user = self.all()
        all_dict = [user.__dict__ for user in all_user]
        return self.__dict__ in all_dict
        # 不能使用self in all_user，因为对象是不可能相同的！！！
        # return self.username == 'gua' and self.password == '123'

        # 直接用前面实现的find_by函数
        # 要记住，尽可能多的复用，类似上面函数中的代码都是零分代码！
        # u = User.find_by(username = self.username)
        # return u is not None and u.password == self.password

        # 而且，上面的零分代码很不好理解！！！
        # us = User.all()
        # for u in us:
        #     if u.username == self.username and u.password == self.password:
        #         return True
        # return False
        # 上面这样写就很好理解！！！
        # 不要吝啬写for循环，清晰明了！

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

def test():
    u = User.find_by(username='gua')
    print(u)

if __name__ == '__main__':
    test()