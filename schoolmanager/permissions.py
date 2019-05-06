from django.conf import settings
from Tools.user_tool import get_user_role
from main.models import CourseDegreeModel,SchoolModel



#只能是学校管理员
class IsSchoolManagerPermission:
    """
    只允许学校管理员访问
    """
    message='权限限制:只允许学校管理员访问.'

    def has_permission(self, request, view):
        school_manager_sign=settings.SCHOOLMANAGER_ROLE
        role=get_user_role(request.user)
        if role==school_manager_sign:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return True


#学校管理员对具体的课时进行操作
class IsSchoolManageAndOwnerPermission:
    """
    只允许学校管理员访问
    """
    message='权限限制:只允许学校管理员并且只能操作自己所负责的学校的课时.'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user_obj=view.request.user
        schools_obj=SchoolModel.objects.filter(user_obj=user_obj)
        coursedegree_obj=CourseDegreeModel.objects.filter(
            course_obj__school_obj__in=schools_obj)
        if coursedegree_obj:
            return True
        else:
            return False




















