from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import get_user_model
from Tools.user_tool import get_num,get_user_role
from UserInfo.models import *


# 登陆验证
class LoginSerialzer(serializers.Serializer):
    mobile_or_email = serializers.CharField(write_only=True,help_text='通过手机号或者电子邮件登陆')
    password=serializers.CharField(write_only=True,help_text='输入登陆密码')

    def validate_mobile_or_email(self, mobile_or_email):
        user_model=get_user_model()
        user_obj=user_model.objects.filter(Q(mobile=mobile_or_email)|Q(email=mobile_or_email)).first()
        if not user_obj:raise serializers.ValidationError('系统没有找到这个账户')
        return user_obj

    def validate(self, data):
        user_obj=data.get('mobile_or_email')
        password=data.get('password')
        is_validate_password=user_obj.check_password(password)
        if is_validate_password:
            self.user_obj=user_obj
            return data
        else:
            raise serializers.ValidationError('密码错误')


#创建用户
class CreateUserSerialzier(serializers.Serializer):
    name=serializers.CharField(allow_null=True,help_text='输入昵称')
    mobile=serializers.CharField(help_text='输入手机号')
    password=serializers.CharField(help_text='输入密码')

    def validate_mobile(self, attrs):
        if get_user_model().objects.filter(mobile=attrs):raise serializers.ValidationError('手机号已经存在')
        return attrs

    def create(self, validated_data):
        temp=get_num(10)
        username=temp
        name=validated_data.get('name',temp)
        mobile=validated_data.get('mobile')
        validate_sign=get_num(10)
        user_model=get_user_model()
        password=validated_data.get('password')
        user_obj=user_model.objects.create(username=username,name=name,
                                  mobile=mobile,validate_sign=validate_sign)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


#用户表的序列化器
class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model=get_user_model()
        fields=('name','mobile','username','mobile','id',)


# 用户表的序列化器
class Users_2_Serializer(serializers.ModelSerializer):
    role=serializers.SerializerMethodField()
    def get_role(self,user_obj):
        return get_user_role(user_obj)

    class Meta:
        model = get_user_model()
        fields = ('id','name', 'mobile', 'mobile','role', )


#权限
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=PermissionModel
        fields=('id','created_at','updated_at','unique_permission_sign',
                'use_allow','move_allow','help','users',)


#角色
class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model=RolesModel
        fields=('id','role_name','users_obj',)


#创造新的角色
class CreateRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model=RolesModel
        fields=('id','role_name',)









