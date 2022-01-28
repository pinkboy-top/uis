"""
用户模块基本功能
"""
import base64
import uuid

from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes
from rest_framework_jwt.views import obtain_jwt_token
from werkzeug.security import generate_password_hash, check_password_hash
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from uis import settings
from user.models import User, UserInfo, Option, OptionType, Img, ImgType
from user.utils.basic import to_dict


@csrf_exempt
def reg_user(res: request):
    """
    注册用户接口
    """
    if res.method == 'POST':
        data = to_dict(res)
        flag = True
        for key in data.keys():
            if data.get(key):
                pass
            else:
                flag = False
                break
        if flag:
            if User.objects.filter(account=data.get('account')):
                return JsonResponse({"code": -10, "msg": "该账号已存在！"}, json_dumps_params={'ensure_ascii': False})
            try:
                img = base64.b64decode(str(data.get('avatar')[0].get('content')).split('base64,')[-1])
                img_name = f'{uuid.uuid4()}.png'
                with open(settings.MEDIA_ROOT + f'/uploads/avatar/{img_name}', 'wb') as f:
                    f.write(img)
            except Exception as e:
                return JsonResponse({'code': -10, 'msg': f'{e}'})
            user = User()
            user.account = data.get('account')
            user.password = generate_password_hash(data.get('password'))
            user.phone = data.get('phone')
            user.save()
            user_info = UserInfo()
            user_info.user_id = user
            user_info.nick_name = data.get('nickname')
            img_obj = Img()
            img_obj.img_url = '/uploads/avatar/{}'.format(img_name)
            img_obj.img_type = ImgType.objects.get(id=1)
            img_obj.save()
            user_info.avatar = img_obj
            user_info.gender = Option.objects.get(id=3) if data.get('gender') == "male" else Option.objects.get(id=4)
            user_info.birthday = data.get("birth_time")
            user_info.summary = data.get("signature")
            user_info.save()
            return JsonResponse({"code": 200, "msg": "注册成功"}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"code": -100, "msg": "参数出错！"}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})


@csrf_exempt
def user_login(res: request):
    """
    用户登录接口
    """
    if res.method == "POST":
        data = to_dict(res)
        flag = True
        for key in data.keys():
            if data.get(key):
                pass
            else:
                flag = False
                break
        if flag:
            try:
                user = User.objects.get(account=data.get('account'))
                if check_password_hash(user.password, data.get('password')):
                    return JsonResponse({"code": 200, "msg": "登录成功"})
                else:
                    return JsonResponse({"code": -10, "msg": "密码或账号错误！"})
            except ObjectDoesNotExist:
                return JsonResponse({"code": -5, "msg": f"账号不存在！"})
    else:
        return JsonResponse({"data": {"code": -100, "msg": f"NO {res.method} METHOD!"}})


@authentication_classes([JSONWebTokenAuthentication])
def home(res: request):
    """
    首页需要携带token
    """
    print(obtain_jwt_token())
    if res:
        return JsonResponse({"data": {"code": 200, "msg": "hello"}})
