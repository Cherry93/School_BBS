# School_BBS
项目基本完善版本

## 欢迎fork / star 如果有问题请Issues 我 或者联系我的qq邮箱：358544104@
# 效果预览
### 主页面

### ![image](https://github.com/Cherry93/images-floor/blob/master/%E4%B8%BB%E9%A1%B5%E9%9D%A2.png)
### 主页面功能包括，发帖，帖子展示，热点信息（爬取网站信息，存入数据库，再显示再页面上，最新评论，热门帖子，按阅读量排序
### 按周、按月、按日进行阅读量排序、帖子默认是原创，帖子有转载功能，点赞，统计阅读量，点赞数，转发数，收藏数。

## 详细页面

### ![image](https://github.com/Cherry93/images-floor/blob/master/%E8%AF%A6%E7%BB%86%E9%A1%B5%E9%9D%A2.png)

### 详细页面有，文章详情，转发，点赞，收藏，帖子的评论，以及二级评论

## 发帖页面
### ![image](https://github.com/Cherry93/images-floor/blob/master/%E5%8F%91%E5%B8%96.png)

### 采用富文本编辑器DjangoUeditor3

### 个人页面

### ![image](https://github.com/Cherry93/images-floor/blob/master/%E4%B8%AA%E4%BA%BA%E9%A1%B5%E9%9D%A2.png)

### 可以对用户信息进行修改，密码修改以及密码重置
### 当然也有用户注册，登录功能，比较常见，就不赘述啦~~~

## 使用步骤：
### django2.0 （版本没啥关系） python3.6（2.7不确定能用不） pillow(图片显示)
### pip install requriements.txt
### 可以先运行星spider 文件的hotinfo.py 会生成一个bbstest.json 这个文件
### python manage.py loaddata bbstest.json 这样数据库就会有你爬下来的数据啦
### 最后python manage.py runserver 
### http://127.0.0.1:8000 就可以看效果了 或者 http://127.0.0.1/index.html
