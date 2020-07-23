from django.shortcuts import render
from . import serializer
from luffyapi.utils.response import APIResponse
from rest_framework.decorators import action
from . import models
from rest_framework.viewsets import ViewSet
import re
from .throttlings import SMSThrottling

# Create your views here.


class LoginView(ViewSet):
    @action(methods=('post',), detail=False)
    def login(self,request, *args, **kwargs):
        ser = serializer.UserSerilaizer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token,username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)


    @action(detail=False)
    def check_telephone(self, request, *args, **kwargs):
        import re
        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}',telephone):
            return APIResponse(code=0, msg='手机号不合法')
        try:
            models.User.objects.get(telephone=telephone)
            return APIResponse(code=1)
        except:
            return APIResponse(code=0, msg='手机号不存在')


    @action(methods=['POST'],detail=False)
    def code_login(self,request,*args,**kwargs):
        ser = serializer.CodeUserSerilaizer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['username']
            return APIResponse(token=token,username=username)
        else:
            return APIResponse(code=0,msg=ser.errors)




from .throttlings import SMSThrottling
class SendSmSView(ViewSet):
    throttle_classes = [SMSThrottling, ]
    @action(methods=['GET'], detail=False)
    def send(self, request, *args, **kwargs):
        from luffyapi.libs.tencent_msg.send import get_code,send_msg
        from django.core.cache import cache
        from django.conf import settings
        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        code = get_code()
        result = send_msg(telephone,code)
        cache.set(settings.PHONE_CACHE_KEY%telephone,code,180)
        if result:
            return APIResponse(code=1, msg='验证码发送成功')
        else:
            return APIResponse(code=0, msg='验证码发送失败')

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
class RegisterView(GenericViewSet,CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserRegisterSerilaizer

    # def create(self, request, *args, **kwargs):
    #     ser=self.get_serializer(data=request.data)
    #     if ser.is_valid():
    #         ser.save()
    #         return APIResponse(code=1,msg='注册成功',username=ser.data.get('username'))
    #     else:
    #         return APIResponse(code=0, msg=ser.errors)



    def create(self, request, *args, **kwargs):
        response=super().create(request, *args, **kwargs)
        username=response.data.get('username')
        return APIResponse(code=1,msg='注册成功',username=username)
