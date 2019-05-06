from rest_framework import serializers
from main.models import ClassNoticeModel
import datetime
from main.models import StudentModel
from django.contrib.auth import get_user_model
from main.models import StudentInfoModel
from main.models import CourseModel
from Tools.serializer_tool import get_user_from_serializer
from main.models import CourseDegreeModel
UserModel=get_user_model()
from schoolmanager.models import SchoolDegreeStartTimeModel
from main.models import SchoolModel,CourseDegreeModel


#学生的通知
class StudentNoticeSerializer(serializers.ModelSerializer):

    show_status=serializers.SerializerMethodField()

    def get_show_status(self,classnotice_obj):
        now=datetime.datetime.now()
        return classnotice_obj.send_end_date>now

    class Meta:
        model=ClassNoticeModel
        fields=('notice','send_start_date','send_end_date','show_status',)


#学生序列化器
class StudentSerializer(serializers.ModelSerializer):
    student_name=serializers.CharField(source='name')
    student_id=serializers.SerializerMethodField()
    class_name=serializers.SerializerMethodField()
    school_name=serializers.SerializerMethodField()
    photo=serializers.ImageField(use_url=False)
    course_names=serializers.SerializerMethodField(help_text='此学生拥有的课程')
    course_ids=serializers.SerializerMethodField(help_text='此学生拥有的课程')

    def get_course_names(self,user_obj):
        courses_obj=CourseModel.objects.filter(studentcoursemodel__student_obj__user_obj=user_obj)
        course_names=['{}|[ID{}]'.format(course_obj.course_name,course_obj.id) for course_obj in courses_obj]
        return course_names

    def get_course_ids(self,user_obj):
        courses_obj=CourseModel.objects.filter(studentcoursemodel__student_obj__user_obj=user_obj)
        course_ids=[course_obj.id for course_obj in courses_obj]
        return course_ids

    def get_student_id(self,user_obj):
        student_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        return student_obj.id

    def get_class_name(self,user_obj):
        student_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        return student_obj.class_obj.class_name

    def get_school_name(self,user_obj):
        student_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        return student_obj.school_obj.school_name

    class Meta:
        model=UserModel
        fields=('class_name','school_name','student_name','student_id',
               'mobile','photo','course_names','course_ids',)


#学生学习记录
class StudentInfoSerializer(serializers.ModelSerializer):

    student_name=serializers.CharField(source='student_obj.user_obj.name')
    log_card_id=serializers.CharField(source='id')

    class Meta:
        model=StudentInfoModel
        fields=('log_card_id',
                'student_obj','student_name',
                'degree_name_log','class_name_log','study_time_log','course_obj_log',
                'course_comment','stage_comment','study',
                'red_card','blue_card','yellow_card',)


#章节序列化器
class DegreeSerializer(serializers.ModelSerializer):
    course_name=serializers.CharField(source='course_obj.course_name')
    degree_start_time=serializers.SerializerMethodField()
    finish_percent=serializers.SerializerMethodField()
    school_name=serializers.SerializerMethodField()
    class_name=serializers.SerializerMethodField()
    teacher_names=serializers.SerializerMethodField()

    def get_teacher_names(self,degree_obj):
        user_obj = get_user_from_serializer(self)
        class_obj=StudentModel.objects.filter(user_obj=user_obj).first().class_obj
        teachers_obj=class_obj.teachermodel_set.all()
        teacher_names=[teacher_obj.user_obj.name for teacher_obj in teachers_obj]
        return teacher_names


    def get_class_name(self,degree_obj):
        user_obj = get_user_from_serializer(self)
        class_obj=StudentModel.objects.filter(user_obj=user_obj).first().class_obj
        return class_obj.class_name

    def get_school_name(self,degree_obj):
        user_obj = get_user_from_serializer(self)
        school_obj = SchoolModel.objects.filter(studentmodel__user_obj=user_obj).first()
        return school_obj.school_name


    def get_finish_percent(self,degree_obj):
        user_obj=get_user_from_serializer(self)
        zong_count=CourseDegreeModel.objects.filter(course_obj=degree_obj.course_obj).count()
        school_obj=SchoolModel.objects.filter(studentmodel__user_obj=user_obj).first()
        degree_start_time_obj=SchoolDegreeStartTimeModel.objects.filter(
            school_obj=school_obj,degree_obj=degree_obj).first()
        this_degree_time=degree_start_time_obj.start_time
        #开课时间位于当前章节开课时间之前的数量,也就是已完成的数量
        finish_count=SchoolDegreeStartTimeModel.objects.filter(
            school_obj=school_obj,
            degree_obj__course_obj=degree_obj.course_obj,
            start_time__lt=this_degree_time).count()
        return '{}/{}'.format(finish_count+1,zong_count)


    def get_degree_start_time(self,degree_obj):

        user_obj=get_user_from_serializer(self)
        school_obj=SchoolModel.objects.filter(studentmodel__user_obj=user_obj).first()
        degree_start_time_obj=SchoolDegreeStartTimeModel.objects.filter(
            school_obj=school_obj,degree_obj=degree_obj).first()
        degree_start_time=degree_start_time_obj.start_time
        return degree_start_time

    class Meta:
        model=CourseDegreeModel
        fields=('course_name','degree_name','remark','degree_start_time',
                'finish_percent','school_name','class_name','teacher_names',)









