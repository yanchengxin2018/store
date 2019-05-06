from rest_framework import viewsets
from Tools import base_tool,user_tool
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import render
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from UserInfo.models import *
from Tools.user_tool import get_user_role
from rest_framework.viewsets import GenericViewSet as G,mixins as M
from rest_framework import serializers


#登陆
class LoginViewSet(base_tool.BaseViewSet):
    '''
    用户登陆
    '''
    serializer_class=LoginSerialzer

    def create(self,request):
        serializer=LoginSerialzer(data=request.data)
        if serializer.is_valid():
            self.user_obj=serializer.user_obj

            token=self.token_handler()

            role=get_user_role(self.user_obj)
            response_data={'token':token,'name':self.user_obj.name,'role':role}
            response=Response(response_data)
            response.set_cookie('token',token)
            return response
        else:
            return Response(serializer.errors)

    def token_handler(self):
        token=user_tool.get_token_from_user(self.user_obj)
        return token


#退出登陆
class LoginOutViewSet(base_tool.BaseViewSet):
    '''
    用户退出登陆
    '''
    def list(self,request):
        response=Response({'success':'已退出登陆'})
        response.delete_cookie('token')
        return response


#注册用户
class RegisterViewSet(base_tool.BaseViewSet):
    serializer_class =CreateUserSerialzier
    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_obj=serializer.save()
            data=UsersSerializer(user_obj).data
            return Response(data)
        else:
            return Response(serializer.errors)


#得到当前用户的信息
class IsLoginViewSet(base_tool.BaseViewSet):

    def list(self, request):
        name=request.user.name if request.user else '游客'
        is_login=True if request.user else False
        return Response({'name':name,'is_login':is_login})


#所有限制权限的接口
class APIViewSet(base_tool.BaseViewSet):

    def list(self, request):
        permission_objs=PermissionModel.objects.all()
        serializer=PermissionSerializer(permission_objs,many=True)
        return Response(serializer.data)


#更新接口权限数据表
class UpdataAPIViewSet(base_tool.BaseViewSet):

    def list(self, request):
        #得到所有应用
        apps=self.get_all_apps()
        #得到应用的所有的权限信息
        permission_infos=self.get_all_permission_info(apps)
        #更新数据表
        self.update_db(permission_infos)
        #没被更新的接口被删除
        self.delete_invalid_data()
        return Response(permission_infos)

    def get_all_apps(self):
        self.apps=settings.MY_APPS
        return self.apps

    def get_all_permission_info(self,apps):
        permission_infos = set()
        for app in apps:
            all_classe_objs=self.get_app_all_classes(app)
            #判断类是否有unique_permission_sign类属性
            for i in all_classe_objs:
                temp=self.is_unique_permission_sign(i)
                if temp:
                    permission_infos.add(temp)
        permission_infos=list(permission_infos)
        i_s=[]
        for i in permission_infos:
            try:
                i[0]
            except:
                continue
            if i[0] in i_s:
                raise serializers.ValidationError(f'{set([j if j[0]==i[0] else "发现重复的标记" for j in permission_infos])}')
            i_s.append(i[0])

        return permission_infos

    def get_app_all_classes(self,app):
        app=self.str_to_obj(app)
        py_files=self.attr_info_delte__(dir(app))
        all_classe_objs=set()
        for py_file in py_files:
            py_file=getattr(app,py_file)
            classes = self.attr_info_delte__(dir(py_file))
            for the_class in classes:
                class_obj=getattr(py_file,the_class)
                all_classe_objs.add(class_obj)
        return all_classe_objs

    def is_unique_permission_sign(self,class_obj):
        unique_permission_sign=getattr(class_obj,'unique_permission_sign',None)
        try:
            unique_permission_sign[0]
        except:
            return None
        return unique_permission_sign

    def update_db(self,permission_infos):
        id_s=[]
        for permission_info in permission_infos:
            unique_permission_sign=permission_info[0]
            id_s.append(unique_permission_sign)
            permissions_obj=self.get_permissions_obj(unique_permission_sign)
            permissions_obj.hlep=permission_info[1]
            permissions_obj.save()
        self.id_s=id_s

    def get_permissions_obj(self,unique_permission_sign):
        permission_obj=PermissionModel.objects.filter(unique_permission_sign=unique_permission_sign).first()
        if permission_obj:
            return permission_obj
        else:
            permission_obj=PermissionModel.objects.create(unique_permission_sign=unique_permission_sign)
            return permission_obj

    def delete_invalid_data(self):
        exact_permission_objs=PermissionModel.objects.exclude(unique_permission_sign__in=self.id_s)
        exact_permission_objs.delete()

    def attr_info_delte__(self,attr_list):
        valid_attrs=[]
        for attr in attr_list[::-1]:
            if attr[:2]!='__':
                valid_attrs.append(attr)
        return valid_attrs

    def str_to_obj(self,order):
        order=f'import {order} as app'
        temp={}
        exec(order,temp)
        app=temp.get('app')
        return app


#用户列表
class UsersViewSet(ModelViewSet):
    queryset = UsersModel.objects.get_queryset().order_by('id')
    serializer_class = Users_2_Serializer


#角色
class RolesViewSet(ModelViewSet):
    queryset = RolesModel.objects.get_queryset().order_by('id')
    serializer_class = RolesSerializer

    def get_serializer_class(self):
        serializer=super().get_serializer_class()
        if self.action=='create':
            return CreateRoleSerializer
        else:
            return serializer


#切换用户
class ChangeUserViewSet(G,M.ListModelMixin):

    def list(self, request, *args, **kwargs):
        mobile=request.GET.get('mobile',None)
        UsersModel=get_user_model()
        user_obj=UsersModel.objects.filter(mobile=mobile).first()
        token = user_tool.get_token_from_user(user_obj)
        role = get_user_role(user_obj)
        response_data = {'token': token, 'name': user_obj.name, 'role': role}
        response = Response(response_data)
        response.set_cookie('token', token)
        return response
































