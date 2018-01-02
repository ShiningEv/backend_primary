from models import Model

# User 和 Message可以存储各种各样的数据
# 想要存储什么样的数据，就定义一个类！

class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')
        self.role = form.get('role', 10)

    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        u = User.find_by(username=self.username)
        # us = User.all()
        # for u in us:
        #     if u.username == self.username and u.password == self.password:
        #         return True
        # return False
        return u is not None and u.password == self.password
        # 这样的代码是不好的，不应该用隐式转换
        # 隐式判断的各种规则，每一种语言都不一样，而且飘忽不定
        # 所以最好全都显式判定，养成良好习惯
        # return u and u.password == self.password
        """
        0 None ''
        """

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

def test():
    # users = User.all()
    # u = User.find_by(username='gua')
    # log('users', u)
    form = dict(
        username='gua',
        password='gua',
    )
    u = User(form)
    u.save()
    # u.save()
    # u.save()
    # u.save()
    # u.save()
    # u.save()
    # u = User.find_by(id=1)
    # u.username = '瓜'
    # u.save()

if __name__ == '__main__':
    test()