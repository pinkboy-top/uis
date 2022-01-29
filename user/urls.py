from django.urls import path

from user.views import reg_user, user_login, home

urlpatterns = [
    path('user/register', reg_user, name="用户注册"),
    path('user/login', user_login, name="用户登录"),
    path('user/home', home, name="用户首页"),
]
