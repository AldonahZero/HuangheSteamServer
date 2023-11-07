"""
    返回结果
    code 类型码 0-成功 1-失败
    data 数据
    msg 提示信息
    kwargs 其他参数
"""
from django.http import JsonResponse

from constant.constants import *


def ok(data=None, msg=MESSAGE_OK, code=0, **kwargs):
    message = {"code": code, "data": data, "msg": msg}
    if kwargs:
        message.update(kwargs)
    return JsonResponse(data=message)


def failed(msg=MESSAGE_FAIL, code=-1, **kwargs):
    message = {"code": code, "data": None, "msg": msg}
    if kwargs:
        message.update(kwargs)
    return JsonResponse(data=message)
