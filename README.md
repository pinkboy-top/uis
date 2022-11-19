# uis
使用Django3.2开发的用户社交系统。
---
---
# 最终实现效果
![前端页面效果]("https://github.com/pinkboy-top/uis/blob/master/news.gif")
---
---
## 包含功能
#### 用户管理
    用户注册
    用户登录
#### 好友功能
    搜索好友
    添加好友
    好友列表
#### 朋友圈
    发送朋友圈
    查看朋友圈
    编辑朋友圈
#### 聊天
    发送文本图片信息


## 安装所需的所有库文件
~~~
pip3 install -r pip_install_list.txt
~~~
## 初始化数据库
~~~
第一步生成数据库描述文件

python manage.py makemigrations

第二步生成实际数据库对应记录

python manage.py migrate

第三步设置后台管理账号

python manage.py createsuperuser
~~~
## 登录后台
~~~
启动开发服务器

python manage.py runserver 80

打开地址

http://127.0.0.1/ylz
~~~
