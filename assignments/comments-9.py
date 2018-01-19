"""
基础 + 熟练度 + 套路 + 工具


后端部分，网页返回由路由支持，而仅仅返回数据则是API的工作


Python的多行字符串''''''并不是一个注释，而是一个字符串，仅仅是没有使用而已


由于js的最初设计不好，使用的时候需要严格遵守，譬如定义变量一定要用var，不然会变成全局变量


MDN文档，不要把字典当知识，每个人都使用了其中的一部分，按需取阅即可


标准套路：js``多行字符串
var todoTemplate = function(todo) {
    var t = `
        <div class="todo-cell">
            <button class="todo-delete">删除</button>
            <span>${todo}</span>
        </div>
    `
    return t
    /*
    上面的写法在 python 中是这样的
    t = '''
    <div class="todo-cell">
        <button class="todo-delete">删除</button>
        <span>{}</span>
    </div>
    '''.format(todo)
    */

}
相比于如下createElement和appendChild，这样的方式更简单、实用，直接生成Template并插入
h = document.createElement('h1')
h.innerHTML = "HAHA"
b.appendChild(h)
实际上可以直接一行：
b.insertAdjacentHTML('beforeend', '<h1>great</h1>')


在此之前，后端版本的todo-list是通过后端的路由函数接收前端的request请求，根据url判断路由函数，返回数据；大多数时间用在路由函数的编写。
而前端版本的todo-list则是完全通过前端的js事件绑定，实现了todo，但缺点是数据没有和后端交互，无法保存。
实际软件开发中，则是需要前后端的紧密配合，实现不同的功能。

"""