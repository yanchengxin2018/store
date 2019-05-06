from main.models import TeacherModel,SchoolModel
from django.conf import settings


#得到这个学校管理员的所有老师用户
def get_teacher_of_school_manager(user_obj):
    return TeacherModel.objects.filter(school_obj__user_obj=user_obj)


#判断这个班级是不是属于这个学校管理员
def class_obj_and_school_manager(class_obj,user_obj):
    school_obj=SchoolModel.objects.filter(classmodel=class_obj,user_obj=user_obj).first()
    return True if school_obj else False


#班级和老师是不是在同一个学校，是不是都属于当前学校管理员
def class_obj_and_user_obj(class_obj,user_obj):
    class_school_obj=class_obj.school_obj
    teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
    teacher_school_obj=teacher_obj.school_obj
    return class_school_obj==teacher_school_obj


#判断这个学校是不是属于这个学校管理员
def school_obj_and_school_manager(school_obj,user_obj):
    school_obj =SchoolModel.objects.filter(pk=school_obj.id,user_obj=user_obj).first()
    return True if school_obj else False


#判断这个老师是不是属于这个学校管理员
def teacher_obj_and_school_manager(teacher_obj,user_obj):
    school_obj=teacher_obj.school_obj
    school_obj =SchoolModel.objects.filter(pk=school_obj.id,user_obj=user_obj).first()
    return True if school_obj else False


#判断这个课程是不是属于这个学校管理员或者是不是属于总部
def course_obj_and_school_manager_or_zongbu(course_obj,user_obj):
    #这个课程所属的学校与学校管理员管辖是否一致
    school_obj=course_obj.school_obj
    if not school_obj:return False
    if school_obj.user_obj==user_obj and user_obj:
        return True
    if course_obj.school_obj.school_name==settings.ZONGBU:
        return True
    return False


#判断这个班级和这个课程是不是在同一个学校
def course_obj_and_class_obj_or_zongbu(course_obj,class_obj):
    course_school_obj=course_obj.school_obj
    class_school_obj=class_obj.school_obj
    if course_obj.school_obj.school_name==settings.ZONGBU:
        return True
    if course_school_obj==class_school_obj and class_school_obj:
        return True
    else:
        return False


#这个学生和这个班级是不是在同一个学校
def student_obj_and_class_obj(student_obj,class_obj):
    student_school_obj=student_obj.school_obj
    class_school_obj=class_obj.school_obj
    if class_school_obj==student_school_obj and class_school_obj:
        return True
    else:
        return False

#这个学生是不是属于这个学校管理员的管辖
def student_obj_and_school_manager(student_obj,user_obj):
    student_school_obj=student_obj.school_obj
    if not student_school_obj:return False
    if student_school_obj.user_obj==user_obj and user_obj:
        return True
    else:
        return False












