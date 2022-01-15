from django.shortcuts import render
from django.http import JsonResponse


def reg_user(request):
    return JsonResponse({"Code": 200, "Msg": "注册成功"})
