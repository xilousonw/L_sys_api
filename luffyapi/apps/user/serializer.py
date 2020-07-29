from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
import re


class UserSerilaizer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username','password','id']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only':True}
        }

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['user'] = user
        return attrs

    def _get_user(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        import re
        if re.match('^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(telephone=username).first()
        elif re.match('^.+@.+$', username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')


    def _get_token(self,user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class CodeUserSerilaizer(serializers.ModelSerializer):
    code = serializers.CharField()
    class Meta:
        model = models.User
        fields = ['telephone', 'code']

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['user'] = user
        return attrs


    def _get_user(self,attrs):

        telephone = attrs.get('telephone')
        code = attrs.get('code')
        cache_code = cache.get(settings.PHONE_CACHE_KET%telephone)#判断验证码一致，通过
        if re.match('^1[3-9][0-9]{9}$', telephone):
            if code==cache_code:
                user = models.User.objects.filter(telephone=telephone).first()
                if user:
                    cache.set(settings.PHONE_CACHE_KEY % telephone,'')#使用过的验证码置空
                    return user
                else:
                    raise ValidationError('用户不存在')
            else:
                raise ValidationError('验证码错误')
        else:
            raise ValidationError('手机不合法')


    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class UserRegisterSerilaizer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4,write_only=True)
    class Meta:
        model = models.User
        fields = ['telephone', 'code', 'password', 'username']
        extra_kwargs = {
            'password': {'max_length':18,'min_length':8},
            'username': {'read_only':True}
        }

    def validate(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code:
            if re.match('^1[3-9][0-9]{9}$', telephone):
                attrs['username'] = telephone
                attrs.pop('code')
                return attrs
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')

    def create(self, validated_data):
        user=models.User.objects.create_user(**validated_data)
        return user

