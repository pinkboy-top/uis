"""
封装一些常用的基本工具
"""
import json

from django.http import request


def to_dict(res: request) -> dict:
    """
    返回处理成字典的request.body数据
    res: 传入一个django的请求对象
    """
    if res.body:
        str_data = res.body.decode('UTF-8')
        return json.loads(str_data)
    else:
        return {}
