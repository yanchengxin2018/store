from django.db import models
from django.contrib.auth.models import AbstractUser



#用户表
class UsersModel(AbstractUser):
    name=models.CharField(max_length=20,help_text='作为昵称')
    mobile=models.CharField(max_length=20,help_text='手机号',unique=True)
    validate_sign=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    photo=models.ImageField(null=True,upload_to='static/teacher')

    def __str__(self):
        return f'{self.name}'


#角色
class RolesModel(models.Model):
    role_name=models.CharField(max_length=20,unique=True)
    users_obj=models.ManyToManyField(to='UsersModel')
    def __str__(self):
        return self.role_name


# 权限
class PermissionModel(models.Model):
    created_at=models.DateTimeField(auto_now=True,help_text='创建时间')
    updated_at=models.DateTimeField(auto_now_add=True,help_text='更新时间')
    unique_permission_sign=models.IntegerField(unique=True,help_text='这个接口的权限代码')
    action_allow=models.CharField(max_length=20,default='ABCDEFG',
                            help_text='[A-GET][B-GET][C-POST][D-PUT][E-PATCH][F-DELTE][G-OPTION]')
    use_allow=models.BooleanField(default=False,help_text='是否允许使用这个权限')
    move_allow=models.BooleanField(default=False,help_text='是否允许转移这个权限')
    help=models.TextField(default='',help_text='关于这个接口的相关说明')
    users=models.ManyToManyField(to='UsersModel')
    def __str__(self):
        return self.help
















