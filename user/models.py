"""
uis系统数据模型
"""
import uuid

from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    基本数据模型包含时间和状态信息
    """
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建日期")
    update_date = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    status = models.BooleanField(default=True, verbose_name="状态")
    is_delete = models.BooleanField(default=False, verbose_name="删除状态")

    class Meta:
        ordering = ["create_date"]
        verbose_name = "基础模型"
        verbose_name_plural = "基础模型"


class User(BaseModel):
    """
    用户基本数据模型
    """
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="用户ID")
    account = models.CharField(max_length=256, unique=True, verbose_name="账号")
    password = models.CharField(max_length=512, editable=False, verbose_name="密码")
    phone = models.CharField(max_length=256, verbose_name="手机号")

    def __str__(self):
        return self.account

    class Meta:
        ordering = ["create_date"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class OptionType(BaseModel):
    """
    选项类型数据模型
    """
    type_name = models.CharField(max_length=256, verbose_name="类型名称")

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ["create_date"]
        verbose_name = "选项类型"
        verbose_name_plural = "选项类型"


class Option(BaseModel):
    """
    选项数据模型
    """
    option_name = models.CharField(max_length=256, verbose_name="选项名称")
    option_type = models.ForeignKey(
        OptionType,
        on_delete=models.CASCADE,
        verbose_name="选项类型"
    )

    def __str__(self):
        return self.option_name

    class Meta:
        ordering = ["create_date"]
        verbose_name = "选项"
        verbose_name_plural = "选项"


class ImgType(BaseModel):
    """
    图片类型数据模型
    """
    type_name = models.CharField(max_length=256, verbose_name="图片类型名称")
    type_path = models.CharField(max_length=256, verbose_name="类型路径")

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ["create_date"]
        verbose_name = "图片类型"
        verbose_name_plural = "图片类型"


class Img(BaseModel):
    """
    图片数据模型
    """
    img_url = models.ImageField(upload_to='uploads/avatar/', verbose_name="图片链接")
    img_type = models.ForeignKey(
        ImgType,
        on_delete=models.CASCADE,
        verbose_name="图片类型"
    )

    def __str__(self):
        return str(self.img_url)

    class Meta:
        ordering = ["create_date"]
        verbose_name = "图片"
        verbose_name_plural = "图片"


class Region(BaseModel):
    """
    地区数据模型
    """
    region_code = models.CharField(max_length=32, unique=True, verbose_name="行政编码")
    region_name = models.CharField(max_length=64, verbose_name="地区名称")
    region_short_name = models.CharField(max_length=32, null=True, verbose_name="地区缩写")
    region_parent_id = models.ForeignKey(
        "Region",
        null=True,
        on_delete=models.CASCADE,
        verbose_name="地区父ID"
    )
    region_level = models.IntegerField(verbose_name="地区级别")

    def __str__(self):
        return self.region_name

    class Meta:
        ordering = ["create_date"]
        verbose_name = "地区"
        verbose_name_plural = "地区"


class Address(BaseModel):
    """
    地址信息数据模型
    """
    region_id = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name="地区"
    )
    address_info = models.CharField(max_length=256, verbose_name="详细地址")
    zip_code = models.CharField(max_length=32, verbose_name="邮政编码")
    address_tag = models.ForeignKey(
        Option,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="地址标签"
    )

    def __str__(self):
        return self.address_info

    class Meta:
        ordering = ["create_date"]
        verbose_name = "地址信息"
        verbose_name_plural = "地址信息"


class UserInfo(BaseModel):
    """
    用户信息数据模型
    """
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="用户信息"
    )
    nick_name = models.CharField(max_length=256, verbose_name="用户昵称")
    avatar = models.ForeignKey(
        Img,
        on_delete=models.CASCADE,
        verbose_name="用户头像"
    )
    gender = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        verbose_name="性别选项"
    )
    birthday = models.DateTimeField(verbose_name="生日")
    summary = models.CharField(max_length=512, default="没有简介。。。。", verbose_name="用户简介")
    email = models.EmailField(null=True, verbose_name="邮箱")
    area = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="用户地区"
    )

    def __str__(self):
        return self.nick_name

    class Meta:
        ordering = ["create_date"]
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"


class Friend(BaseModel):
    """
    好友数据模型
    """
    me = models.OneToOneField(
        User,
        related_name="me",
        on_delete=models.CASCADE,
        verbose_name="自己"
    )
    friends = models.ManyToManyField(
        User,
        related_name="friends",
        verbose_name="好友"
    )

    def __str__(self):
        return self.me.account

    class Meta:
        ordering = ["create_date"]
        verbose_name = "好友"
        verbose_name_plural = "好友列表"


class FriendRequest(BaseModel):
    """好友请求数据模型"""
    request_user = models.ForeignKey(
        User,
        related_name="request_user",
        on_delete=models.CASCADE,
        verbose_name="请求好友"
    )
    add_user = models.ForeignKey(
        User,
        related_name="add_user",
        on_delete=models.CASCADE,
        verbose_name="被添加好友"
    )
    request_text = models.CharField(max_length=256, verbose_name="请求留言")
    is_ok = models.BooleanField(default=False, verbose_name="是否处理")
    expired_date = models.DateTimeField(verbose_name="过期日期")

    def __str__(self):
        return self.request_text

    class Meta:
        ordering = ["create_date"]
        verbose_name = "好友请求"
        verbose_name_plural = "好友请求"


class News(BaseModel):
    """
    动态消息数据模型
    """
    title = models.CharField(max_length=512, null=True, verbose_name="标题")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="作者"
    )
    friend_view_list = models.ManyToManyField(
        User,
        related_name="friend_view_list",
        verbose_name="好友查看列表"
    )
    friend_like_list = models.ManyToManyField(
        User,
        related_name="friend_like_list",
        verbose_name="好友点赞列表"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["create_date"]
        verbose_name = "动态消息"
        verbose_name_plural = "动态消息数据模型"


class File(BaseModel):
    """
    文件数据模型
    """
    file_name = models.CharField(max_length=256, verbose_name="文件名称")
    file_content = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        verbose_name="文件内容"
    )
    file_type = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        verbose_name="文件类型"
    )
    related_news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name="关联动态消息"
    )

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["create_date"]
        verbose_name = "文件"
        verbose_name_plural = "文件数据"


class Comment(BaseModel):
    """
    评论模型
    评论留言
    好友评论
    回复评论
    """
    comment_news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name="关联动态消息"
    )
    content = models.CharField(max_length=256, verbose_name="回复内容")
    comment_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_user",
        verbose_name="评论用户")
    aims_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="aims_user",
        verbose_name="目标用户"
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "用户评论"

