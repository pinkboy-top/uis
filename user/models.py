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


class User(BaseModel):
    """
    用户基本数据模型
    """
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="用户ID")
    name = models.CharField(max_length=256, verbose_name="用户名")
