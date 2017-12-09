# 2017/02/18
# 作业 2
# ========
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    queryList = []
    for key, value in query.items():
        queryList.append("{}={}".format(key, value))
    return path + "?" + "&".join(queryList)


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典


# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    headerStr = ""
    for key, value in headers.items():
        headerStr = headerStr + "{}: {}\r\n".format(key, value)
    return headerStr

# 作业 2.4
#
# 为作业 2.3 写测试
def test_header_from_dict():
    headers = {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    expected = 'Content-Type: text/html\r\nContent-Length: 127\r\n'
    e = "header_from_dict Error: \n({}) \n({})".format(header_from_dict(headers), expected)
    assert header_from_dict(headers) == expected, e

# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client_ssl.py 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
<span class="title">\xe6\x98\x9f\xe9\x99\x85\xe7\xa9\xbf\xe8\xb6\x8a</span><span class="title">&nbsp;/&nbsp;Interstellar</span><span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>\n
<span class="other">&nbsp;/&nbsp;\xe6\x98\x9f\xe9\x99\x85\xe5\x90\xaf\xe7\xa4\xba\xe5\xbd\x95(\xe6\xb8\xaf)  /  \xe6\x98\x9f\xe9\x99\x85\xe6\x95\x88\xe5\xba\x94(\xe5\x8f\xb0)</span>
2，分数
<span class="rating_num" property="v:average">9.2</span>
3，评价人数
<div class="star">
        <span class="rating5-t"></span>
        <span class="rating_num" property="v:average">9.5</span>
        <span property="v:best" content="10.0"></span>
        <span>432257人评价</span>
</div>
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）
<p class="quote">
    <span class="inq">最好的宫崎骏，最好的久石让。 </span>
</p>

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""
def body_parser(body):
    # 1，电影名
    name_list = []
    re.search('<span class="title">&nbsp;/&nbsp;(.*)</span>', body).group

# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""

def test():
    test_path_with_query()
    test_header_from_dict()

if __name__ == "__main__":
    test()