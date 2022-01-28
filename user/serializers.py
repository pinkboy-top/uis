"""
默认序列化模块
"""
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    用户模型序列化类
    """
    class Meta:
        model = User
        fields = ('uid', 'account', 'phone')
