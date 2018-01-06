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
        return u is not None and u.password == self.salted_password(self.password)
        # 这样的代码是不好的，不应该用隐式转换
        # 隐式判断的各种规则，每一种语言都不一样，而且飘忽不定
        # 所以最好全都显式判定，养成良好习惯
        # return u and u.password == self.password
        """
        0 None ''
        """

    def validate_register(self):
        if len(self.username) > 2 and len(self.password) > 2:
            self.password = self.salted_password(self.password)
            if User.find_by(username=self.username) is None:
                return True
            else:
                return False

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        """$!@><?>HUI&DWQa`"""
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2


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