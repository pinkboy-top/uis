from django.urls import path

from user.views import reg_user, user_login, home, get_user_info, search_friend, add_friend_request, get_friend_request,\
    confirm_add_request, get_friend_list, post_news, get_news

urlpatterns = [
    path('user/register', reg_user, name="用户注册"),
    path('user/login', user_login, name="用户登录"),
    path('user/home', home, name="用户首页"),
    path('user/user_info', get_user_info, name="用户详情"),
    path('user/search_friend', search_friend, name="搜索好友"),
    path('user/add_friend_request', add_friend_request, name="添加好友请求"),
    path('user/get_friend_request', get_friend_request, name="获取好友请求"),
    path('user/confirm_add_request', confirm_add_request, name="同意好友请求"),
    path('user/get_friend_list', get_friend_list, name="获取好友列表"),
    path('user/post_news', post_news, name="发送动态信息"),
    path('user/get_news', get_news, name="获取动态信息")
]
