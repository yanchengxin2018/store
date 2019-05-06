from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from UserInfo.models import UsersModel
from UserInfo.serializers import UsersSerializer
from Tools.user_tool import invalid_token
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet,GenericViewSet as G
from rest_framework.views import APIView
from django.shortcuts import render


#测试
class TestViewSet(ModelViewSet):

    unique_permission_sign=(1452,'正在测试权限')
    serializer_class = TestSerializer
    queryset = TestModel.objects.get_queryset().order_by('id')

    def list(self,request,*args,**kwargs):
        import os
        n = os.system('main/re_start.sh')
        # n = os.system('echo522 "Hello World !"')
        print('--->',n)
        order=request.GET.get('order',None)
        if order:order=int(order)
        if order==1:
            self.order_1()
            return Response('用户表已清除')
        elif order==2:
            user_obj=request.user
            if user_obj:
                return Response(f'当前用户为{user_obj.username}|{user_obj.mobile}|{user_obj.name}')
            else:
                return Response('当前用户身份为游客')
        elif order==3:
            data=UsersSerializer(get_user_model().objects.all(),many=True).data
            return Response(data)
        elif order==4:
            return self.order_4()
        elif order==0:
            return self.order_0()
        else:
            info_01=f'欢迎你,{request.user.name if request.user else "游客"}!<br><br>'
            info_1='<a href="http://{}/api/test?order=1">清空用户表</a><br><br>'.format(settings.IP)
            info_2='<a href="http://{}/api/test?order=2">查看我是谁</a><br><br>'.format(settings.IP)
            info_3='<a href="http://{}/api/test?order=3">查看所有的用户</a><br><br>'.format(settings.IP)
            info_4='<a href="http://{}/api/test?order=4">使当前用户的token失效</a><br><br>'.format(settings.IP)
            info_0='<a href="http://{}/api/test?order=0">核实验1区</a><br><br>'.format(settings.IP)

            info=info_01+info_1+info_2+info_3+info_0+info_4
            return HttpResponse(info)

    def order_1(self):
        UsersModel.objects.all().delete()

    def order_4(self):
        invalid_token(self.request.user)
        return Response('当前token在任何网页失去了作用')

    def order_0(self):
        # CourseModel.objects.all().delete()
        return Response('')


#开发用的主页
class IndexViewSet(APIView):
    def get(self,request):
        user_obj=request.user
        if user_obj:
            info_1='欢迎你,{}!'.format(request.user)
            info_2='更换账户'
        else:
            info_1='还没有登陆'
            info_2='点击登陆'
        data={'info_1':info_1,'info_2':info_2}
        return render(request,'index.html',data)



























