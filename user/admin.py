from django.contrib import admin

# Register your models here.
from user.models import User, UserInfo, OptionType, Option, ImgType, Img, Friend, FriendRequest, News, File, Comment, \
Region, Address, Message, Chat, Group

# 设置站点后台标题
admin.site.site_header = "荔枝"
admin.site.site_title = "荔枝"

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(OptionType)
admin.site.register(Option)
admin.site.register(ImgType)
admin.site.register(Img)
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(News)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Region)
admin.site.register(Address)
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Group)
