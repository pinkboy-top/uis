"""
默认序列化模块
"""
from rest_framework import serializers

from user.models import User, UserInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    用户模型序列化类
    """
    class Meta:
        model = User
        fields = ('uid', 'account', 'phone')


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    """
    用户详情模型序列化类
    """
    class Meta:
        model = UserInfo
        fields = ('uid', 'nick_name', 'avatar', 'gender', 'birthday', 'summary', 'account', 'phone')
        depth = 1
