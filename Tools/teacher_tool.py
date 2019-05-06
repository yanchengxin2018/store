from main.models import TeacherModel
import datetime
from rest_framework import serializers


#班级和老师是不是有关系
def class_obj_and_teacher_obj(class_obj,user_obj):
    teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
    if not teacher_obj:return False
    class_obj=teacher_obj.class_obj.filter(pk=class_obj.id).first()
    return True if class_obj else False


#得到今天的开头和结尾
def get_today():
    now=datetime.datetime.now()
    start_time = datetime.datetime.strptime(f'{now.year}-{now.month}-{now.day}', '%Y-%m-%d')
    time_long=datetime.timedelta(days=1)
    end_time=start_time+time_long
    return start_time,end_time


#这个学生是不是这个老师教的
def student_obj_and_teacher_obj(student_obj,user_obj):
    teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
    if not teacher_obj:raise serializers.ValidationError({'error':'无效的老师账户'})
    students_class_obj=student_obj.class_obj
    classes_obj=teacher_obj.class_obj.all()
    if classes_obj.filter(pk=students_class_obj.id).first():
        return True
    else:
        return False