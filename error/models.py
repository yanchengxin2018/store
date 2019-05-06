from django.db import models
from django.contrib.auth import get_user_model
user_model=get_user_model()


#异常记录
class ExceptionLogModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True,help_text='创建时间') #
    user_obj=models.ForeignKey(user_model,on_delete=models.SET_NULL,null=True,help_text='出现异常的用户') #
    url=models.TextField(help_text='原始的访问URL',null=True) #
    post_data=models.BinaryField(help_text='被转化为文本的post的数据',null=True) #
    get_data=models.BinaryField(help_text='被转化为文本的get的数据',null=True)
    header_data=models.BinaryField(help_text='被转化为文本的header的数据',null=True) #
    cookie_data=models.BinaryField(help_text='被转化为文本的cookie的数据',null=True)
    exception_data=models.BinaryField(help_text='记录异常的提示信息',null=True)
    action=models.CharField(max_length=10,null=True,help_text='请求方式')
    status=models.CharField(max_length=10,null=True,help_text='状态码')







