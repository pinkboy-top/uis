"""
自定义文件上传大小限制检测中间件
"""
from django.http import JsonResponse
from django.core.exceptions import RequestDataTooBig


class CheckRequest(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, RequestDataTooBig):
            return JsonResponse({"code": -99, "msg": "超过文件上传最大限制！"})
