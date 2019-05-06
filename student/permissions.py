from main.models import StudentModel


#只允许学生访问
class IsStudentPermission:

    message='只允许学生访问这个接口'

    def has_permission(self,request,view):
        if not request.user:return False
        student_obj=StudentModel.objects.filter(user_obj=request.user).first()
        return bool(student_obj)

    def has_object_permission(self,request,view,obj):
        return True




