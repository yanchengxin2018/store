from UserInfo.models import UsersModel
from rest_framework import serializers
from main.models import TeacherModel,ClassModel,StudentModel,StudentInfoModel,ClassNoticeModel
import os
from error import custom_errors
from teacher.tools import get_student_edit_status,get_stage_status
from Tools.serializer_tool import get_user_from_serializer
from schoolmanager.models import SchoolDegreeStartTimeModel
import datetime


#当前老师的用户信息只读的
class MyInfoReadOnlySerializer(serializers.ModelSerializer):
    photo=serializers.SerializerMethodField()
    mobile=serializers.CharField(read_only=True)
    classes=serializers.SerializerMethodField()

    def get_classes(self,user_obj):
        teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:raise serializers.ValidationError({'error':'没有找到这个老师'})
        classes_obj=teacher_obj.class_obj.all()
        return [class_obj.class_name for class_obj in classes_obj]
    def get_photo(self,user_obj):
        from django.conf import settings
        return '{}/{}'.format(settings.IP,user_obj.photo)

    class Meta:
        model=UsersModel
        fields=('name','mobile','photo','classes',)

#当前老师用户的信息
class MyInfoSerializer(serializers.ModelSerializer):


    class Meta:
        model=UsersModel
        fields=('name','photo',)

    def update(self, instance, validated_data):
        try:
            path=instance.photo.path
        except:
            path=None
        user_obj=super().update(instance, validated_data)
        try:
            if (not path==instance.photo.path) and path:
                os.remove(path)
        except:
            pass
        return user_obj


#班级序列化器
class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model=ClassModel
        fields=('id','class_name',)


#学生的序列化器
class StudentSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='user_obj.name',read_only=True)
    student_obj=serializers.CharField(source='id')
    class_name=serializers.CharField(source='class_obj.class_name',read_only=True)
    school_name=serializers.CharField(source='class_obj.school_obj.school_name')


    class Meta:
        model=StudentModel
        fields=('student_obj','name','class_obj','class_name','school_name',)


#学生信息(包含阶段测评)
class StudentInfoSerializer(serializers.ModelSerializer):

    stage_status=serializers.SerializerMethodField()
    edit_status=serializers.SerializerMethodField()

    #应该有一个字段记录几天是不是有课
    def validate(self, datas):
        fields=['red_card', 'blue_card', 'yellow_card']
        for field in fields:
            field=datas.get(field,None)
            if not field:continue
            if field<0 or field>5:
                raise custom_errors.Status_403('卡片数量的范围应该在0-5之间')
        return datas

    #这个学生是否有阶段性测评字段
    def get_stage_status(self,studentinfo_obj):
        return get_student_edit_status(studentinfo_obj.student_obj)

    def get_edit_status(self,studentinfo_obj):
        return get_student_edit_status(studentinfo_obj.student_obj)

    def update(self, instance, validated_data):
        #如果这个学生没有阶段性评测,那么提交的阶段性修改是无效的
        student_obj=instance.student_obj
        if not get_stage_status(student_obj):
            stage_comment=validated_data.pop('stage_comment',None)
            if stage_comment:raise custom_errors.Status_400('此学生今日没有阶段性评测.请勿提交无效数据.')

        #准备数据
        today=datetime.date.today()
        today_start=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        one_day=datetime.timedelta(days=1)
        today_end=today_start+one_day

        #筛选今日对应的学习章节
        school_defree_start_time_obj=SchoolDegreeStartTimeModel.objects.filter(
            #定位学生
            degree_obj__course_obj__studentcoursemodel__student_obj=student_obj,
            #定位时间
            start_time__gt=today_start,
            start_time__lt=today_end).first()
        if not school_defree_start_time_obj:
            raise custom_errors.Status_503


        #得到字段
        class_name = student_obj.class_obj.class_name
        degree=school_defree_start_time_obj.degree_obj.degree_name
        course_obj=school_defree_start_time_obj.degree_obj.course_obj
        study_time=school_defree_start_time_obj.start_time

        if not instance.class_name_log:
            validated_data['class_name_log']=class_name
        if not instance.degree_name_log:
            validated_data['degree_name_log']=degree
        if not instance.study_time_log:
            validated_data['study_time_log']=study_time
        if not instance.course_obj_log:
            validated_data['course_obj_log']=course_obj
        return super().update(instance, validated_data)


    class Meta:
        model=StudentInfoModel
        fields=('student_obj','red_card','blue_card','yellow_card',
                'course_comment','stage_comment','study','stage_status','edit_status',
                'class_name_log','degree_name_log','study_time_log',)
        read_only_fields=('student_obj','class_name_log','degree_name_log','study_time_log',)


#班级的通知序列化器
class ClassNoticeSerialzier(serializers.ModelSerializer):

    class_name=serializers.CharField(source='class_obj.class_name',read_only=True)

    def validate_class_obj(self, class_obj):
        user_obj=get_user_from_serializer(self)
        teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
        classes_obj=teacher_obj.class_obj.all()
        class_obj=classes_obj.filter(id=class_obj.id).first()
        if not class_obj:raise custom_errors.Status_401('当前老师没有权限操作这个班级')
        return class_obj

    class Meta:
        model=ClassNoticeModel
        fields=('id','class_obj','class_name','notice','send_start_date','send_end_date',)



