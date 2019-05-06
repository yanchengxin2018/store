from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.views.static import serve
from django.http import HttpResponse

import json,datetime,os
from main import views as main_views

from UserInfo.user_urls import user_router
from manager.manager_urls import manager_router
from schoolmanager.schoolmanager_urls import schoolmanager_router
from teacher.teacher_urls import teacher_router
from error.error_urls import error_router
from vue.vue_urls import vue_router
from student.student_urls import student_router
from makeonline.makeonline_urls import makeonline_router


#时json处理不支持的类型实例
class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        #如果对象是datetime.datetime类型,进行以下处理
        if isinstance(obj, datetime.datetime):
            time_str=obj.strftime('%Y-%m-%dT%H:%M')
            return time_str
        else:
            return json.JSONEncoder.default(self, obj)


#使用测试
def test(request):
    now=datetime.datetime.now()
    json_data=json.dumps(now,cls=CustomEncoder)
    print(json_data)    #这里输出  "2019-03-20T17:03"

    return HttpResponse('xxx')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    url(r'^users/',include(user_router.urls)),                      #关于用户账户的一切路由
    url(r'^manager/',include(manager_router.urls)),                 #关于管理员的一切路由
    url(r'^schoolmanager/',include(schoolmanager_router.urls)),     #关于学校管理员的一切路由
    url(r'^teacher/',include(teacher_router.urls)),                 #关于老师的一切路由
    url(r'^error/',include(error_router.urls)),                     #关于老师的一切路由
    url(r'^vue/',include(vue_router.urls)),                         #关于vue的一切路由
    url(r'^student/',include(student_router.urls)),                 #关于学生的一切路由
    url(r'^makeonline/',include(makeonline_router.urls)),           #关于在线编译的一切路由

    path('admin/', admin.site.urls),                                                          #admin主页
    url(r'^static/(?P<path>.+)$',serve,{"document_root":os.path.join(BASE_DIR, 'static/')}),  #静态文件路由
    url(r'test',test),                                                                        #测试接口
    url(r'^index', main_views.IndexViewSet.as_view()),                                        #文档主页
]
