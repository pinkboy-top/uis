"""
封装一些常用的基本工具
"""
import os
import datetime
import json
import base64
import hashlib
import uuid
from asgiref.sync import sync_to_async
from collections.abc import Callable

from django.http import request, JsonResponse
from loguru import logger

from uis.settings import JWT_TOKEN, MEDIA_ROOT, FILE_TYPE
from user.models import User, UserInfo, Chat, Message, Option


def to_dict(res: request) -> dict:
    """
    返回处理成字典的request.body数据
    res: 传入一个django的请求对象
    """
    # logger.info(res.body)
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
    if args:
        for key in args.keys():
            if args.get(key) is None:
                return False
        return True
    else:
        return False


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


def verify_token(key: bytes, token: str) -> bool:
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
        logger.info(e)
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


def login_auth(func: Callable) -> Callable:
    """
    登录验证装饰器，验证是否登录，是否有权限
    """

    def is_login(res: request) -> [Callable, request]:
        result = func
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
        else:
            return JsonResponse({"code": -5, "msg": "token错误!"})
        return result(res)

    return is_login


def upload_file(ba64_str: str, f_type: str, f_path: str) -> [str, bool]:
    """
    上传文件函数，需要传入已经Base64编码的字符串
    ba64_str: Base64编码的字符串
    file_type: 上传的文件类型
    file_path: 上传的文件存放路径
    return: 返回文件路径加名称或者失败的状态
    """
    if f_type not in FILE_TYPE:
        return False
    try:
        img = base64.b64decode(ba64_str)
        img_name = f'{uuid.uuid4()}.{f_type}'
        # 文件夹不存在就创建
        to_path = rf"{MEDIA_ROOT + f_path}"
        if not os.path.exists(to_path):
            os.makedirs(to_path)
        with open(to_path + img_name, 'wb') as f:
            f.write(img)
        return f'{f_path}{img_name}'
    except Exception as e:
        logger.info(e)
        return False


def get_client_ip(res: request) -> str:
    """
    获取用户请求的ip地址
    """
    x_forwarded_for = res.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = res.META.get('REMOTE_ADDR')
    return ip


def get_user_data(res: request) -> [dict, str]:
    """
    获取用户数据
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    token = res.META.get("HTTP_AUTHORIZATION")
    user = User.objects.get(account=get_payload(token).get("data").get("account"))
    data = to_dict(res)
    result = {
        "user": user,
        "data": data
    }
    return result


def file_path():
    """
    返回文件存储路径
    """
    return os.path.join(MEDIA_ROOT, 'files')


@sync_to_async
def save_msg(msg: str, bind_uid: str, chat_id: int, is_read=False) -> bool:
    """
    保存消息
    """
    msg_obj = Message()
    option = Option.objects.filter(option_name="文本信息")
    chat_id = Chat.objects.filter(pk=chat_id)

    msg_obj.content = msg
    msg_obj.content_type = option[0]
    msg_obj.bind_user = User.objects.get(uid=bind_uid)
    msg_obj.msg_chat = chat_id[0]
    msg_obj.is_read = is_read

    msg_obj.save()

    return True


@sync_to_async
def get_msg(chat_id: int) -> list:
    """
    获取消息
    """
    chat = Chat.objects.filter(pk=chat_id)
    message = Message.objects.filter(msg_chat=chat_id, is_read=False)

    if message:
        result = []
        send_user = UserInfo.objects.get(user_id=chat.send_user)
        accept_user = UserInfo.objects.get(user_id=chat.accept_user)

        for item in message:
            result.append({
                "msg": item.content,
                "chat_id": chat.id,
                "send_user_avatar": send_user.avatar.img_url.url,
                "accept_user_avatar": accept_user.avatar.img_url.url,
                "accept_user_nick_name": accept_user.nick_name,
                "send_user_nick_name": send_user.nick_name,
                "accept_user_id": accept_user.user_id.uid,
                "send_user_id": send_user.user_id.uid,
                "send_user_account": send_user.user_id.account,
                "accept_user_account": accept_user.user_id.account
            })

            # 将消息更新为已读
            item.is_read = True
            item.save()
        return result


@logger.catch
def test():
    logger.info("测试日志")
    raise "测试错误！"


if __name__ == "__main__":
    # cache = get_token({"data": {"name": "pink"}})
    # print(cache)
    # print(verify_token(b'pink-boy', cache))
    test()
