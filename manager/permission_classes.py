from django.conf import settings
from Tools.user_tool import get_user_role


#仅允许总管理员访问
class IsManagerPermission:
    """
    只允许总管理员访问
    """
    message='权限限制:只允许总管理员访问.'

    def has_permission(self, request, view):
        manager_sign=settings.MANAGER_ROLE
        role=get_user_role(request.user)
        if role==manager_sign:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return True