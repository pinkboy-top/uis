"""
用户模块基本功能
"""
import datetime
import time

from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash

from uis.settings import logger
from user.models import User, UserInfo, Option, Img, ImgType, Friend, FriendRequest
from user.utils.basic import to_dict, verify_args, get_token, login_auth, get_payload, upload_file, get_client_ip


@csrf_exempt
def reg_user(res: request):
    """
    注册用户接口
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    data = to_dict(res)
    if verify_args(data) is False:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "没有参数！"})
    if User.objects.filter(account=data.get('account')):
        logger.info(f"{get_client_ip(res)}:{data.get('account')}")
        return JsonResponse({"code": -10, "msg": "该账号已存在！"}, json_dumps_params={'ensure_ascii': False})
    ba64_str = str(data.get('avatar')[0].get('content')).split('base64,')[-1]
    file_type = str(data.get('avatar')[0].get('content').split(';base64')[0].split('/')[-1])
    img_name = upload_file(ba64_str, file_type, '/uploads/avatar/')
    if img_name is False:
        return JsonResponse({'code': -99, 'msg': '不允许上传的文件类型！'})
    user = User()
    user.account = data.get('account')
    user.password = generate_password_hash(data.get('password'))
    user.phone = data.get('phone')
    user.save()
    user_info = UserInfo()
    user_info.user_id = user
    user_info.nick_name = data.get('nickname')
    img_obj = Img()
    img_obj.img_url = img_name
    img_obj.img_type = ImgType.objects.get(id=1)
    img_obj.save()
    user_info.avatar = img_obj
    user_info.gender = Option.objects.get(id=3) if data.get('gender') == "male" else Option.objects.get(id=4)
    user_info.birthday = data.get("birth_time")
    user_info.summary = data.get("signature")
    user_info.save()
    logger.info(f"{get_client_ip(res)}:{data.get('account')}")
    return JsonResponse({"code": 200, "msg": "注册成功"}, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def user_login(res: request):
    """
    用户登录接口
    """
    if res.method != "POST":
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    data = to_dict(res)
    if verify_args(data) is False:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "没有参数！"})
    try:
        user = User.objects.get(account=data.get('account'))
        if check_password_hash(user.password, data.get('password')):
            # 签发的token有效期是12小时
            token = get_token({"exp": time.time() + 60 * 60 * 12, "data": {"account": user.account}})
            logger.info(f"{get_client_ip(res)}: {data.get('account')}")
            return JsonResponse({"code": 200, "msg": "登录成功", "data": {"token": token}})
        else:
            logger.info(f"{get_client_ip(res)}: {data.get('account')}")
            return JsonResponse({"code": -10, "msg": "密码或账号错误！"})
    except ObjectDoesNotExist:
        logger.info(f"{get_client_ip(res)}: {data.get('account')}")
        return JsonResponse({"code": -5, "msg": "账号不存在！"})


@login_auth
def home(res: request):
    """
    首页需要携带token
    """
    if res:
        return JsonResponse({"data": {"code": 200, "msg": "hello"}})


@csrf_exempt
@login_auth
def get_user_info(res: request):
    """
    获取用户详情
    """
    if res.method != "POST":
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    token = res.META.get("HTTP_AUTHORIZATION")

    # 获取token中的数据
    user = User.objects.get(account=get_payload(token).get("data").get("account"))
    user_info = UserInfo.objects.get(user_id=user.uid)
    result = {
        "account": user.account,
        "nickname": user_info.nick_name,
        "avatar": f"http://{res.get_host()}{user_info.avatar.img_url.url}",
        "gender": user_info.gender.option_name,
        "summary": user_info.summary,
        "birthday": user_info.birthday.strftime("%y-%m-%d"),
        "create_date": user_info.create_date.strftime("%y-%m-%d")
    }
    logger.info(f"{get_client_ip(res)}: {user_info.nick_name}")
    return JsonResponse({'code': 200, 'msg': 'security', 'data': result}, safe=False)


@csrf_exempt
@login_auth
def search_friend(res: request):
    """
    搜索好友
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    data = to_dict(res)
    if verify_args(data) is False:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "没有参数！"})
    try:
        account = data.get("account")
        if account:
            user = User.objects.get(account=account)
            user_info = UserInfo.objects.get(user_id=user.uid)
            result = {
                "uid": user.uid,
                "account": user.account,
                "nick_name": user_info.nick_name,
                "avatar": f"http://{res.get_host()}{user_info.avatar.img_url.url}",
                "gender": user_info.gender.option_name,
                "summary": user_info.summary,
                "birthday": user_info.birthday.strftime("%y-%m-%d"),
                "create_date": user_info.create_date.strftime("%y-%m-%d")
            }
            logger.info(f"{get_client_ip(res)}: {user_info.nick_name}")
            return JsonResponse({'code': 200, 'msg': 'security', 'data': result}, safe=False)
    except ObjectDoesNotExist:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": 100, "msg": "账号不存在！"})


@csrf_exempt
@login_auth
def add_friend_request(res: request):
    """
    添加好友请求
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    data = to_dict(res)
    if verify_args(data) is False:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "没有参数！"})
    try:
        token = res.META.get("HTTP_AUTHORIZATION")
        request_user = User.objects.get(account=get_payload(token).get("data").get("account"))
        request_user_info = UserInfo.objects.get(user_id=request_user)
        # logger.info(request_user_info.nick_name)
        add_user = User.objects.get(account=data.get("add_user"))
        request_text = f"{request_user_info.nick_name}请求添加你为好友"
        friend_request = FriendRequest.objects.filter(add_user=add_user, request_user=request_user, is_ok=False)
        friend = Friend.objects.filter(me=request_user, friends=add_user)
        if len(friend_request) > 0:
            return JsonResponse({"code": 100, "msg": "请勿重复提交好友添加请求！"})
        if len(friend) > 0:
            return JsonResponse({"code": 100, "msg": "该用户已经是你的好友！"})
        if request_user.pk == add_user.pk:
            return JsonResponse({"code": 100, "msg": "不能添加自己为好友！"})
        # 在好友请求里面添加一条对应的好友请求记录
        add_request = FriendRequest()
        add_request.request_user = request_user
        add_request.add_user = add_user
        add_request.request_text = request_text
        # 过期时间是一个星期
        add_request.expired_date = datetime.datetime.now() + datetime.timedelta(days=7)
        add_request.save()
        return JsonResponse({'code': 200, 'msg': '好友请求已发送'}, safe=False)
    except ObjectDoesNotExist:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "账号不存在！"})


@csrf_exempt
@login_auth
def get_friend_request(res: request):
    """
    获取好友添加请求
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    token = res.META.get("HTTP_AUTHORIZATION")
    add_user = User.objects.get(account=get_payload(token).get("data").get("account"))
    now_date = datetime.datetime.now()
    friend_request = FriendRequest.objects.filter(add_user=add_user, is_ok=False, expired_date__gte=now_date)
    if len(friend_request) == 0:
        return JsonResponse({"code": 200, "msg": "no request！"})
    result = []
    for val in friend_request:
        user_info = UserInfo.objects.get(user_id=val.request_user)
        result.append({
            "request_id": val.pk,
            "request_user": val.request_user.uid,
            "nick_name": user_info.nick_name,
            "avatar": f"http://{res.get_host()}{user_info.avatar.img_url.url}",
            "summary": user_info.summary,
            "add_user": val.add_user.uid,
            "request_text": val.request_text,
            "is_ok": val.is_ok,
            "expired_date": val.expired_date
        })
    return JsonResponse({'code': 200, 'msg': 'security', 'data': result}, safe=False)


@csrf_exempt
@login_auth
def confirm_add_request(res: request):
    """
    确认添加好友请求同意或者拒绝好友请求
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    data = to_dict(res)
    if verify_args(data) is False:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "没有参数！"})
    try:
        token = res.META.get("HTTP_AUTHORIZATION")
        request_id = data.get("request_id")
        is_ok = data.get("is_ok")
        user = User.objects.get(account=get_payload(token).get("data").get("account"))
        # logger.info(request_id)
        # 取到对应的好友请求
        friend_request = FriendRequest.objects.get(pk=request_id)
        if is_ok is False:
            friend_request.is_ok = True
            friend_request.save()
            return JsonResponse({'code': 200, 'msg': '您已拒绝该用户的好友添加请求。'}, safe=False)
        my_friend = Friend.objects.filter(me=user)
        # logger.info(my_friend)
        # 第一次添加好友需要创建好友列表
        if len(my_friend) == 0:
            my_friend = Friend()
            my_friend.me = user
            # 多对多先保存再绑定
            my_friend.save()
            my_friend.friends.add(friend_request.request_user)
            friend_request.is_ok = True
            friend_request.save()
            return JsonResponse({'code': 200, 'msg': '您已经同意该用户的好友添加请求。'}, safe=False)
        else:
            my_friend[0].me = user
            my_friend[0].friends.add(friend_request.request_user)
            my_friend[0].save()
            friend_request.is_ok = True
            friend_request.save()
            # logger.info(friend_request.request_user)
            return JsonResponse({'code': 200, 'msg': '您已经同意该用户的好友添加请求。'}, safe=False)
    except ObjectDoesNotExist:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "账号不存在！"})


@csrf_exempt
# @logger.catch
@login_auth
def get_friend_list(res: request):
    """
    获取好友列表
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})

    token = res.META.get("HTTP_AUTHORIZATION")
    user = User.objects.get(account=get_payload(token).get("data").get("account"))

    my_friend = Friend.objects.filter(me=user)
    if len(my_friend) == 0:
        logger.info(f"{get_client_ip(res)}: 没有好友")
        # 第一次需要创建好友列表
        my_friend = Friend()
        my_friend.me = user
        my_friend.save()
        # 找到所有好友列表里面存在我自己的数据全部更新到自己的好友模型
        friends = Friend.objects.filter(friends=user)
        for friend in friends:
            my_friend.friends.add(friend.me)
            my_friend[0].save()
        return JsonResponse({"code": 100, "msg": "no friend!"})

    # 每次获取好友列表都将添加的好友进行更新
    friends = Friend.objects.filter(friends=user)
    for friend in friends:
        my_friend[0].friends.add(friend.me)
        my_friend[0].save()
    result = []
    for val in my_friend[0].friends.all():
        user_info = UserInfo.objects.get(user_id=val)
        result.append({
            "uid": val.uid,
            "account": val.account,
            "nick_name": user_info.nick_name,
            "avatar": f"http://{res.get_host()}{user_info.avatar.img_url.url}",
            "summary": user_info.summary,
            "gender": user_info.gender.option_name
        })
    return JsonResponse({'code': 200, 'msg': 'security', 'data': result}, safe=False)


@csrf_exempt
@login_auth
def post_news(res: request):
    """
    发送动态信息
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    token = res.META.get("HTTP_AUTHORIZATION")
    user = User.objects.get(account=get_payload(token).get("data").get("account"))

    data = to_dict(res)
    if verify_args(data) is False:
        logger.info(f"{get_client_ip(res)}: {data}")
        return JsonResponse({"code": -5, "msg": "没有参数！"})
    title = data.get("title")
    files = data.get("files")
    for f in files:
        try:
            print(f)
            return JsonResponse({'code': 200, 'msg': 'security', 'data': title}, safe=False)
        except Exception as e:
            return JsonResponse({'code': -10, 'msg': '{}'.format(e)})


@csrf_exempt
@login_auth
def get_news(res: request):
    """
    获取动态信息
    """
    if res.method != 'POST':
        logger.info(f"{get_client_ip(res)}: 非法请求！")
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})
    token = res.META.get("HTTP_AUTHORIZATION")
    user = User.objects.get(account=get_payload(token).get("data").get("account"))
    return JsonResponse({'code': 200, 'msg': 'security'}, safe=False)
