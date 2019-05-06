from Tools.user_tool import get_user_role
from django.conf import settings


#只允许老师用户访问这个接口
class IsTeacherPermission:

    message='只允许老师用户访问这个接口'

    def has_permission(self,request,view):
        try:
            role=get_user_role(request.user)
            return role==settings.TEACHER_ROLE
        except:
            return False

    def has_object_permission(self,request,view,obj):
        return True


#只允许老师用户访问这个接口并且只能查看自己的信息
class IsTeacherAndReadSelfOnlyPermission:

    message='只允许老师用户访问这个接口'

    def has_permission(self,request,view):
        try:
            role=get_user_role(request.user)
            return role==settings.TEACHER_ROLE
        except:
            return False

    def has_object_permission(self,request,view,obj):
        try:
            return request.user==obj
        except:
            return False















