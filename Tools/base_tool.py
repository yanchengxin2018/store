from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.conf import settings
from UserInfo.models import RolesModel
from rest_framework.pagination import PageNumberPagination
import pickle
import requests,json


#分页类
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 300


# 视图集基类
class BaseViewSet(viewsets.ViewSet):
    unique_permission_sign=None
    """
    示例 viewset 演示了将由路由器类处理的标准动作。
    如果你使用格式后缀，请务必为每个动作包含一个`format=None` 的关键字参数。
    """
    def list(self, request):
        raise serializers.ValidationError({'error':'不允许的请求方式'})

    def create(self, request):
        raise serializers.ValidationError({'error':'不允许的请求方式'})

    def retrieve(self, request, pk=None):
        raise serializers.ValidationError({'error':'不允许的请求方式'})

    def update(self, request, pk=None):
        raise serializers.ValidationError({'error':'不允许的请求方式'})

    def partial_update(self, request, pk=None):
        raise serializers.ValidationError({'error':'不允许的请求方式'})

    def destroy(self, request, pk=None):
        raise serializers.ValidationError({'error':'不允许的请求方式'})


#统一错误处理
class ErrorHandler:
    pass


def errorhandler(error):
    raise ValidationError(error)


#得到老师角色的对象
def get_teacher_role_obj():
    teacher_role=settings.TEACHER_ROLE
    teacher_role_obj=RolesModel.objects.filter(role_name=teacher_role).first()
    if teacher_role_obj:
        return teacher_role_obj
    else:
        teacher_role_obj=RolesModel.objects.create(role_name=teacher_role)
        return teacher_role_obj


#得到学生角色的对象
def get_student_role_obj():
    student_role=settings.STUDENT_ROLE
    student_role_obj=RolesModel.objects.filter(role_name=student_role).first()
    if student_role_obj:
        return student_role_obj
    else:
        student_role_obj=RolesModel.objects.create(role_name=student_role)
        return student_role_obj


#发送短信验证码
class SendSMS:

    def __init__(self,mobile,data,log=False):
        self.test=settings.CODE_TEST
        account=settings.CODE_USER
        pswd=settings.CODE_PASSWORD
        self.url='http://120.27.244.164/msg/HttpBatchSendSM'
        log='瓦力工厂' if not log else log
        self.text='【{}】{}'.format(log,data)
        self.args={'account':account,'pswd':pswd,'mobile':mobile,
                   'msg':self.text,'needstatus':'True','resptype':'json'}
        self.get_url()

    def get_url(self):
        args_all=''
        for key in self.args:
            args='{}={}&'.format(key,self.args[key])
            args_all=args_all+args
        self.url=self.url+'?'+args_all[:-1]

    def send(self):
        if self.test:
            return self.test_send()
        response = requests.get(self.url)
        data=json.loads(response.text)
        status=data.get('result',400)

        #status为空时返回True
        if not status:
            return True
        #status不为空时代表有错误发生.生成错误信息并返回False告诉调用者发送失败了
        else:
            error={103:'提交过快（同时时间请求验证码的用户过多）',104:'短信平台暂时不能响应请求',
                   107:'包含错误的手机号码',109:'无发送额度（请联系管理员）',110:'不在发送时间内',
                   111:'短信数量超出当月发送额度限制，请联系管理员',400:'运营商没有返回正确的参数'}
            error_info=error.get(status)
            if error_info:
                self.error_info=error_info
            else:
                self.error_info='未知错误'
            return False

    def test_send(self):
        print('短信模块暂时不可用,程序即将启动模拟发送')
        info='模拟发送：向[{}]的手机号发送了[{}]'.format(self.args.get('mobile'),self.text)
        print(info)
        return True






