"""
封装一些常用的基本工具
"""
import datetime
import json
import base64
import hashlib
from collections.abc import Callable

from django.http import request, JsonResponse
from uis.settings import JWT_TOKEN


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


def verify_args(args: dict) -> bool:
    """
    验证前端提交的数据完整性
    args: 前端提交的数据，已经转字典
    """
    for key in args.keys():
        if args.get(key):
            pass
        else:
            return False
    return True


def to_ba64(d_str: str) -> bytes:
    """
    返回编码后的base64字节对象
    d_str：待装换成base64编码的字符串
    """
    en_str = d_str.encode()
    bs_str = base64.b64encode(en_str)
    return bs_str


def ba64_to_str(b_str: str) -> str:
    """
    返回base64解码后的字符串数据
    """
    return base64.b64decode(b_str.encode()).decode()


def hash_util(key, d_str) -> str:
    """
    hash256计算工具函数
    key：加密的key是字节对象
    d_str：待哈希的字符串字节对象
    """
    hash_obj = hashlib.sha256(key)
    hash_obj.update(d_str)
    return hash_obj.hexdigest()


class Token(object):
    """
    创建token类实现token的生成校验
    """

    def __init__(self, header: str, payload: str, key: bytes):
        """
        初始化方法，需要传入生成token的三个必要参数
        header：token的头部需要标识加密的算法和类型
        payload: token的有效载荷部分需要过期时间签发者创建的时间戳签发的面向群体可以自定义需要的键值对
        """
        self.header = header
        self.payload = payload
        self.key = key

    def json_str_sign(self) -> str:
        """
        对json字符串进行签名
        """
        b_header = to_ba64(self.header)
        b_payload = to_ba64(self.payload)
        b_group = b_header + b'.' + b_payload
        return hash_util(self.key, b_group)

    def create_token(self):
        """
        创建token
        """
        jwt_token = to_ba64(self.header) + b'.' + to_ba64(self.payload) + b'.' + to_ba64(self.json_str_sign())
        return jwt_token


def get_token(reload: dict) -> str:
    """
    获取自定义签发token
    payload: 自定义载荷数据，可重载过期时间，自定义数据段
    """
    header = json.dumps(JWT_TOKEN.get("header"))
    temp = JWT_TOKEN.get("payload")
    temp.update(reload)
    payload = json.dumps(temp)
    # 实例化token类传入自定义私钥，创建token字符串返回
    jwt_token = Token(header, payload, b'pink-boy')
    return jwt_token.create_token().decode()


def verify_token(key: bytes, token: str):
    """
    token验证函数，验证签发的token是否是本人签发
    验证原理是逆向一遍编码的token传入相同的hash秘钥判断生成的token是否相同
    token：token字符串客户端传入的token
    """
    try:
        temp = token.split(".")
        header = ba64_to_str(temp[0])
        payload = ba64_to_str(temp[1])
        # 实例化token类传入自定义私钥，创建token字符串返回
        jwt_token = Token(header, payload, key)
        if token == jwt_token.create_token().decode():
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def get_payload(token: str) -> dict:
    """
    获取token中的自定义载荷
    b64_str: base64编码后的payload数据段
    """
    if token:
        temp = token.split(".")
        payload = ba64_to_str(temp[1])
        return json.loads(payload)
    else:
        return {}


def login_auth(func: Callable):
    """
    登录验证装饰器，验证是否登录，是否有权限
    """

    def is_login(res: request):
        result = func(res)
        token = res.META.get("HTTP_AUTHORIZATION")
        if token is None:
            return JsonResponse({"code": -1, "msg": "未登录!"})
        # 验证token是否过期
        if verify_token(b'pink-boy', token):
            now_time = datetime.datetime.now()
            flag_time = get_payload(token).get("exp")
            exp_time = datetime.datetime.fromtimestamp(flag_time)
            if now_time > exp_time:
                return JsonResponse({"code": -5, "msg": "登录已过期!"})
        return result
    return is_login


if __name__ == "__main__":
    cache = get_token({"data": {"name": "pink"}})
    print(cache)
    print(verify_token(b'pink-boy', cache))
