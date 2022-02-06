from django.contrib import admin

# Register your models here.
from user.models import User, UserInfo, OptionType, Option, ImgType, Img

# 设置站点后台标题
admin.site.site_header = "测试系统"
admin.site.site_title = "荔枝"

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(OptionType)
admin.site.register(Option)
admin.site.register(ImgType)
admin.site.register(Img)
