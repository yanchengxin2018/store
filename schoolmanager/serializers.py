from rest_framework import serializers
from main.models import StudentModel,TeacherModel,ClassModel,SchoolModel,ClassCourseModel
from UserInfo.models import UsersModel
from Tools.base_tool import errorhandler
from Tools.user_tool import get_user_role
from Tools.serializer_tool import get_user_from_serializer,get_view_from_serializer
from Tools.base_tool import get_teacher_role_obj,get_student_role_obj
from main.models import CourseModel,CourseDegreeModel
from django.conf import settings
from UserInfo.serializers import CreateUserSerialzier
from Tools.schoolmanager_tool import class_obj_and_school_manager,teacher_obj_and_school_manager
from Tools.schoolmanager_tool import course_obj_and_school_manager_or_zongbu,\
    course_obj_and_class_obj_or_zongbu,student_obj_and_class_obj,student_obj_and_school_manager
from main.models import StageClassModel,StageSchoolModel
from error import custom_errors
from schoolmanager.models import SchoolDegreeStartTimeModel,StudentCourseModel


# 班级
class ClassSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)

    class Meta:
        model = ClassModel
        fields = ('id', 'class_name','school_obj','school_name',)

    def validate_school_obj(self, school_obj):

        user=get_user_from_serializer(self)
        school_obj=SchoolModel.objects.filter(id=school_obj.id,user_obj=user).first()
        if not school_obj:raise serializers.ValidationError({'error':'当前学校管理员无权操作这个学校'})
        return school_obj


#班级学生绑定
class ClassStudentSerilaizer(serializers.ModelSerializer):
    name=serializers.CharField(source='user_obj.name',read_only=True)

    class Meta:
        model=StudentModel
        fields=('name','user_obj','class_obj',)

    def validate_user_obj(self, attrs):
        user_obj=UsersModel.objects.filter(pk=attrs).first()
        if not user_obj:return errorhandler({'error':'没有这个用户'})
        role=get_user_role(user_obj)
        from django.conf import settings
        if role != settings.STUDENT_ROLE:
            return errorhandler({'error':'角色必须为{}'.format(settings.STUDENT_ROLE)})
        return user_obj


#学校
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolModel
        fields=('id','school_name',)


#老师
class TeacherSerializer(serializers.ModelSerializer):
    school_obj=serializers.CharField(write_only=True)
    school_name=serializers.SerializerMethodField()

    def get_school_name(self,user_obj):
        teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:return None
        return teacher_obj.school_obj.school_name

    class Meta:
        model=UsersModel
        fields=('id','name','mobile','school_obj','school_name',)

    def validate_school_obj(self, school_id):
        #这个学校是不是属于这个管理员管理
        user_obj=get_user_from_serializer(self)
        school_obj=SchoolModel.objects.filter(pk=school_id,user_obj=user_obj).first()
        if not school_obj:raise serializers.ValidationError({'error':'当前学校管理员没有权限操作这个班级'})
        return school_obj

    def create(self, validated_data):
        #创建用户
        user_obj=self.create_user(validated_data)
        # 添加角色
        self.create_role(user_obj)
        # 绑定学校
        self.create_school(validated_data,user_obj)
        return user_obj

    #创建用户
    def create_user(self,validated_data):
        validated_data['password']=123456
        serializer=CreateUserSerialzier(data=validated_data)
        if serializer.is_valid():
            user_obj=serializer.save()
            return user_obj
        else:
            raise serializers.ValidationError({'error':serializer.errors})

    #添加角色
    def create_role(self,user_obj):
        try:
            get_teacher_role_obj().users_obj.add(user_obj)
        except:
            raise serializers.ValidationError({'error':'创建失败'})

    #绑定班级
    def create_school(self,validated_data,user_obj):
        school_obj=validated_data.get('school_obj')
        teacher_obj = TeacherModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:
            teacher_obj=TeacherModel.objects.create(user_obj=user_obj,school_obj=school_obj)
        teacher_obj.save()


#学生
class StudentSerializer(serializers.ModelSerializer):
    school_obj=serializers.CharField(write_only=True)
    school_name=serializers.SerializerMethodField()
    student_obj=serializers.SerializerMethodField()

    def get_student_obj(self,user_obj):
        student_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        return student_obj.id

    def get_school_name(self,user_obj):
        teacher_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:return None
        return teacher_obj.school_obj.school_name

    class Meta:
        model=UsersModel
        fields=('id','name','mobile','school_obj','school_name','student_obj',)

    def validate_school_obj(self, school_id):
        #这个学校是不是属于这个管理员管理
        user_obj=get_user_from_serializer(self)
        school_obj=SchoolModel.objects.filter(pk=school_id,user_obj=user_obj).first()
        if not school_obj:raise serializers.ValidationError({'error':'当前学校管理员没有权限操作这个学校'})
        return school_obj

    def create(self, validated_data):
        #创建用户
        user_obj=self.create_user(validated_data)
        # 添加角色
        self.create_role(user_obj)
        # 绑定学校
        self.create_school(validated_data,user_obj)
        return user_obj

    #创建用户
    def create_user(self,validated_data):
        validated_data['password']=123456
        serializer=CreateUserSerialzier(data=validated_data)
        if serializer.is_valid():
            user_obj=serializer.save()
            return user_obj
        else:
            raise serializers.ValidationError({'error':serializer.errors})

    #添加角色
    def create_role(self,user_obj):
        try:
            get_student_role_obj().users_obj.add(user_obj)
        except:
            raise serializers.ValidationError({'error':'创建失败'})

    #绑定班级
    def create_school(self,validated_data,user_obj):
        school_obj=validated_data.get('school_obj')
        teacher_obj = StudentModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:
            teacher_obj=StudentModel.objects.create(user_obj=user_obj,school_obj=school_obj)
        teacher_obj.save()


#本校的课程管理
class CourseSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)
    class Meta:
        model=CourseModel
        fields=('id','course_name','school_obj','school_name',)

    def validate_school_obj(self, school_obj):
        user_obj=get_user_from_serializer(self)
        if not user_obj:raise serializers.ValidationError('未知错误')
        school_obj=SchoolModel.objects.filter(pk=school_obj.id,user_obj=user_obj).first()
        if not school_obj:raise serializers.ValidationError('当前学校管理员没有操作这所学校的权限')
        return school_obj


#章节
class CourseDegreeSerializer(serializers.ModelSerializer):
    course_name=serializers.CharField(source='course_obj.course_name',read_only=True)

    class Meta:
        model=CourseDegreeModel
        fields=('id','degree_name','course_obj','remark','course_name',)

    def validate_course_obj(self, course_obj):
        user_obj=get_user_from_serializer(self)
        schools_obj=SchoolModel.objects.filter(user_obj=user_obj)
        if CourseModel.objects.filter(pk=course_obj.id,school_obj__in=schools_obj):
            return course_obj
        else:
            raise serializers.ValidationError({'error':'当前学校管理员没有操作这个课程的权限'})

    def update(self, instance, validated_data):
        if validated_data.pop('course_obj',None):
            raise custom_errors.Status_401({'error':'更新操作不能更改course_obj'})
        return super().update(instance, validated_data)

#设置某个学校里章节的开课时间
class SchoolDegreeStartTimeSerializer(serializers.ModelSerializer):

    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)
    degree_name=serializers.CharField(source='degree_obj.degree_name',read_only=True)

    def validate_school_obj(self, school_obj):
        user_obj=get_user_from_serializer(self)
        if school_obj.user_obj!=user_obj:raise custom_errors.Status_401({'error':'当前学校管理员没有权限管理这个学校'})
        return school_obj

    def validate(self,data):
        degree_obj=data.get('degree_obj',None)
        school_obj=data.get('school_obj',None)
        zongbu=settings.ZONGBU
        if degree_obj.course_obj.school_obj==zongbu:return data
        if degree_obj.course_obj.school_obj==school_obj:return data
        raise custom_errors.Status_403({'error':'此章节所属课程既不属于总部亦不属于当前学校,无法建立关联'})


    class Meta:
        model=SchoolDegreeStartTimeModel
        fields=('id','school_name','degree_name','school_obj','degree_obj','start_time',)


#更新课时
class DegreeUpdateSerialzier(serializers.ModelSerializer):

    class Meta:
        model=CourseDegreeModel
        fields=('id','degree_name','remark',)


#显示班级和老师
class ClassTeacherSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='user_obj.name',read_only=True)
    mobile=serializers.CharField(source='user_obj.mobile',read_only=True)
    is_relevance=serializers.SerializerMethodField()

    #是否和传过来的class_id有关系
    def get_is_relevance(self,teacher_obj):
        view=get_view_from_serializer(self)
        class_id=view.request.GET.get('class_obj',None)
        if not class_id:raise serializers.ValidationError({'error':'需要在get参数里提供班级id(calss_obj)'})
        classes_obj=teacher_obj.class_obj.all()
        try:
            class_obj=classes_obj.filter(pk=class_id).first()
        except:
            raise serializers.ValidationError({'error':'检查class_obj是否是有效的整数'})
        return True if class_obj else False

    class Meta:
        model=TeacherModel
        fields=('user_obj','name','mobile','is_relevance',
                'class_obj',)


#绑定班级和老师
class CreateClassTeacherSerializer(serializers.Serializer):
    class_obj=serializers.IntegerField(write_only=True)
    user_obj=serializers.IntegerField(write_only=True)
    relevance = serializers.BooleanField(write_only=True,help_text='绑定或者解绑班级和老师的关系')

    def validate_class_obj(self, class_id):
        class_obj=ClassModel.objects.filter(pk=class_id).first()
        if not class_obj:raise serializers.ValidationError({'error':'不存在这个班级'})
        user_obj=get_user_from_serializer(self)
        if class_obj_and_school_manager(class_obj,user_obj):
            return class_obj
        else:
            raise serializers.ValidationError({'error':'当前学校管理员没有权限管理这个班级'})

    def validate_user_obj(self, user_id):
        user_obj=UsersModel.objects.filter(pk=user_id).first()
        teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:raise serializers.ValidationError({'error':'不存在这个老师'})
        user_obj=get_user_from_serializer(self)
        if teacher_obj_and_school_manager(teacher_obj,user_obj):
            return teacher_obj
        else:
            raise serializers.ValidationError({'error':'当前学校管理员没有权限操作这个老师'})

    def create(self, validated_data):
        relevance = validated_data.get('relevance')
        teacher_obj = validated_data.get('user_obj')
        class_obj = validated_data.get('class_obj')
        if relevance:
            teacher_obj.class_obj.add(class_obj)
            teacher_obj.save()
            return teacher_obj
        else:
            teacher_obj=TeacherModel.objects.filter(user_obj=teacher_obj.user_obj).first()
            teacher_obj.class_obj.remove(class_obj.id)
            return teacher_obj


#显示班级和课程
class ClassCourseSerializer(serializers.ModelSerializer):
    is_relevance=serializers.SerializerMethodField()
    course_obj=serializers.CharField(source='id',read_only=True)
    # school_name=serializers.CharField(source='school_obj.school_name')

    #是否和传过来的class_id有关系
    def get_is_relevance(self,course_obj):
        #班级id和当前课程是不是有关系
        #班级课程表是否有这俩货
        view = get_view_from_serializer(self)
        class_id = view.request.GET.get('class_obj', None)
        if not class_id: raise serializers.ValidationError({'error': '需要在get参数里提供班级id(calss_obj)'})
        try:
            class_obj=ClassModel.objects.filter(pk=class_id).first()
        except:
            raise serializers.ValidationError({'error':'检查class_obj是否是有效的整数'})
        user_obj=get_user_from_serializer(self)
        if not class_obj_and_school_manager(class_obj,user_obj):
            raise serializers.ValidationError({'error':'当前学校管理员没有权限管理这个班级'})
        if not course_obj_and_school_manager_or_zongbu(course_obj,user_obj):
            raise serializers.ValidationError({'error':'这个课程不属于当前管理员的学校并且不属于总部'})
        classcourse_obj=ClassCourseModel.objects.filter(class_obj=class_obj,course_obj=course_obj).first()
        return True if classcourse_obj else False

    class Meta:
        model=CourseModel
        fields=('course_obj','course_name','is_relevance',)


#绑定班级和课程
class CreateClassCourseSerializer(serializers.Serializer):
    class_obj=serializers.IntegerField(write_only=True)
    course_obj=serializers.IntegerField(write_only=True)
    relevance = serializers.BooleanField(write_only=True)

    def validate_class_obj(self, class_id):
        class_obj=ClassModel.objects.filter(pk=class_id).first()
        if not class_obj:raise serializers.ValidationError({'error':'不存在这个班级'})
        user_obj=get_user_from_serializer(self)
        if class_obj_and_school_manager(class_obj,user_obj):
            return class_obj
        else:
            raise serializers.ValidationError({'error':'当前学校管理员没有权限管理这个班级'})

    def validate_course_obj(self, course_id):
        course_obj=CourseModel.objects.filter(pk=course_id).first()
        if not course_obj:raise serializers.ValidationError({'error':'不存在这个课程'})
        user_obj=get_user_from_serializer(self)
        if not course_obj_and_school_manager_or_zongbu(course_obj,user_obj):
            raise serializers.ValidationError({'error':'这个课程不属于这个学校管理员并且不属于总部'})
        else:
            return course_obj

    def create(self, validated_data):
        relevance = validated_data.get('relevance')
        course_obj = validated_data.get('course_obj')
        class_obj = validated_data.get('class_obj')
        if not course_obj_and_class_obj_or_zongbu(course_obj,class_obj):
            raise serializers.ValidationError({'error':'课程和班级不在同一个学校并且此课程也不在总部'})

        if relevance:
            classcourse_obj=ClassCourseModel.objects.create(course_obj=course_obj,class_obj=class_obj)
            return classcourse_obj
        else:
            classcourse_obj =ClassCourseModel.objects.filter(course_obj=course_obj,
                                                             class_obj=class_obj).first()
            if classcourse_obj:
                classcourse_obj.delete()
            return classcourse_obj


#显示班级和学生
class ClassStudentSerializer(serializers.ModelSerializer):
    is_relevance=serializers.SerializerMethodField()
    name=serializers.CharField(source='user_obj.name')
    student_obj=serializers.CharField(source='user_obj.id')
    mobile=serializers.CharField(source='user_obj.mobile')
    class_name=serializers.SerializerMethodField()
    def get_class_name(self,student_obj):
        class_obj=student_obj.class_obj
        if class_obj:
            return class_obj.class_name
        else:
            return '暂时没有分配班级'


    #是否和传过来的class_id有关系
    def get_is_relevance(self,student_obj):
        #班级id和当前学生是不是有关系
        #班级学生表是否有这俩货
        view = get_view_from_serializer(self)
        class_id = view.request.GET.get('class_obj', None)
        if not class_id: raise serializers.ValidationError({'error': '需要在get参数里提供班级id(calss_obj)'})
        try:
            class_obj=ClassModel.objects.filter(pk=class_id).first()
        except:
            raise serializers.ValidationError({'error':'检查class_obj是否是有效的整数'})
        user_obj=get_user_from_serializer(self)
        if not class_obj_and_school_manager(class_obj,user_obj):
            raise serializers.ValidationError({'error':'当前学校管理员没有权限管理这个班级'})
        if not student_obj_and_class_obj(student_obj,class_obj):
            raise serializers.ValidationError({'error':'此学生和班级不在同一个学校里'})

        student_class_obj=student_obj.class_obj
        if student_class_obj==class_obj:
            return True
        else:
            return False

    class Meta:
        model=StudentModel
        fields=('name','student_obj','mobile','is_relevance','class_name',)


#绑定班级和学生
class CreateClassStudentSerializer(serializers.Serializer):
    class_obj=serializers.IntegerField(write_only=True)
    student_obj=serializers.IntegerField(write_only=True)
    relevance = serializers.BooleanField(write_only=True)

    def validate_class_obj(self, class_id):
        class_obj=ClassModel.objects.filter(pk=class_id).first()
        if not class_obj:raise serializers.ValidationError({'error':'不存在这个班级'})
        user_obj=get_user_from_serializer(self)
        if class_obj_and_school_manager(class_obj,user_obj):
            return class_obj
        else:
            raise serializers.ValidationError({'error':'当前学校管理员没有权限管理这个班级'})

    def validate_student_obj(self, student_id):
        user_obj=UsersModel.objects.filter(pk=student_id).first()
        student_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        if not student_obj:raise serializers.ValidationError({'error':'没有找到这个学生'})
        user_obj=get_user_from_serializer(self)
        if not student_obj_and_school_manager(student_obj,user_obj):
            raise serializers.ValidationError({'error':'这个学生不属于这个学校管理员的管辖'})
        else:
            return student_obj

    def create(self, validated_data):
        relevance = validated_data.get('relevance')
        student_obj = validated_data.get('student_obj')
        class_obj = validated_data.get('class_obj')
        if not student_obj_and_class_obj(student_obj,class_obj):
            raise serializers.ValidationError({'error':'学生和班级不在同一个学校'})
        if relevance:
            student_obj.class_obj=class_obj
        else:
            student_obj.class_obj=None
        student_obj.save()
        return student_obj


#为班级的阶段性评测设置一个时间点
class StageClassSerializer(serializers.ModelSerializer):

    class_name=serializers.CharField(source='class_obj.class_name',read_only=True)
    school_name=serializers.CharField(source='class_obj.school_obj.school_name',read_only=True)
    comment_time=serializers.CharField()

    def validate_class_obj(self, class_obj):

        #验证一下,操作的这个班级是不是属于这个学校管理员
        #检查用户是不是有权力管理这个班级
        user_obj=get_user_from_serializer(self)
        if not class_obj_and_school_manager(class_obj=class_obj,user_obj=user_obj):
            raise custom_errors.Status_403({'error':'这个班级不在当前学校管理员的管理范围'})
        else:
            return class_obj

    class Meta:
        model=StageClassModel
        fields=('id','school_name','class_name','class_obj','comment_time',)


#为学校的阶段性评测设置一个时间点
class StageSchoolSerializer(serializers.ModelSerializer):

    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)

    def validate_school_obj(self, school_obj):
        #验证一下,操作的这个班级是不是属于这个学校管理员
        #检查用户是不是有权力管理这个班级
        user_obj=get_user_from_serializer(self)
        if school_obj.user_obj==user_obj:
            return school_obj
        else:
            raise custom_errors.Status_401({'error':'这所学校并不属于当前学校管理员'})

    class Meta:
        model=StageSchoolModel
        fields=('id','school_name','school_obj','comment_time',)


#学生拥有的课程
class StudentCourseSerializer_(serializers.ModelSerializer):

    student_name=serializers.CharField(source='student_obj.user_obj.name',read_only=True)
    student_mobile=serializers.CharField(source='student_obj.user_obj.mobile',read_only=True)
    course_name=serializers.CharField(source='course_obj.course_name',read_only=True)
    bind=serializers.BooleanField(write_only=True,help_text='提交真值绑定,提交假值解绑')

    class Meta:
        model=StudentCourseModel
        fields=('id','student_obj','course_obj','student_name','course_name','student_mobile','bind',)

    def validate_student_obj(self, student_obj):
        try:
            user_obj_1=student_obj.school_obj.user_obj
        except:
            raise custom_errors.Status_401({'error': '此学生不在当前学校管理员的管理范围'})
        user_obj_2=get_user_from_serializer(self)
        if user_obj_1!=user_obj_2:
            raise custom_errors.Status_401({'error':'此学生不在当前学校管理员的管理范围'})
        return student_obj

    def validate_course_obj(self, course_obj):
        zongbu=settings.ZONGBU
        course__school_obj=course_obj.school_obj
        #如果课程所属的学校为空,返回401
        if not course__school_obj:raise custom_errors.Status_401({'error':'此课程没有所属学校,你没有权限操作它'})
        #如果这个课程属于总部,允许使用
        if course__school_obj.school_name==zongbu:
            return course_obj
        #如果课程所属的学校还没有学校管理员,返回401
        course__user_obj=course__school_obj.user_obj
        if not course__user_obj:raise custom_errors.Status_401({'error':'此课程所属的学校没有管理员,你没有权限操作它'})
        # 如果课程所属的学校管理员与当前用户相同,允许使用
        this_user_obj=get_user_from_serializer(self)
        if course__user_obj==this_user_obj:
            return course_obj
        else:
            raise custom_errors.Status_401({'error':'此课程不在当前用户的管理权限之内'})

    def validate(self, attrs):
        attrs.pop('bind')
        return super().validate(attrs)


#绑定学生和课程(只读)
class StudentCourseSerializer(serializers.ModelSerializer):
    is_relevance=serializers.SerializerMethodField()
    course_obj=serializers.CharField(source='id')
    student_obj=serializers.SerializerMethodField()
    # serializers.SerializerMethodField

    def get_student_obj(self,course_obj):
        view_obj=get_view_from_serializer(self)
        student_id = view_obj.request.GET.get('student_obj', None)
        return student_id

    def get_is_relevance(self,course_obj):
        view_obj=get_view_from_serializer(self)
        student_id=view_obj.request.GET.get('student_obj',None)
        try:
            studentcourse_obj=StudentCourseModel.objects.filter(course_obj=course_obj,student_obj__id=student_id).first()
        except:
            raise custom_errors.Status_400({'error':'student_obj参数不能被服务器理解'})
        return bool(studentcourse_obj)

    class Meta:
        model=CourseModel
        fields=('course_name','is_relevance','course_obj','student_obj',)


#绑定班级和课程(只写)
class StudentCourseWriteOnlySerializer(serializers.Serializer):
    student_obj=serializers.IntegerField(write_only=True)
    course_obj=serializers.IntegerField(write_only=True)
    relevance = serializers.BooleanField(write_only=True)

    def validate_student_obj(self, student_id):
        student_obj=StudentModel.objects.filter(pk=student_id).first()
        if not student_obj:raise custom_errors.Status_404({'error':'不存在这个学生'})
        user_obj=get_user_from_serializer(self)
        if student_obj_and_school_manager(student_obj,user_obj):
            return student_obj
        else:
            raise custom_errors.Status_401({'error':'当前学校管理员没有权限管理这个学生'})

    def validate_course_obj(self, course_id):
        course_obj=CourseModel.objects.filter(pk=course_id).first()
        if not course_obj:raise serializers.ValidationError({'error':'不存在这个课程'})
        user_obj=get_user_from_serializer(self)
        if not course_obj_and_school_manager_or_zongbu(course_obj,user_obj):
            raise serializers.ValidationError({'error':'这个课程不属于这个学校管理员并且不属于总部'})
        else:
            return course_obj

    def create(self, validated_data):
        relevance = validated_data.get('relevance')
        course_obj = validated_data.get('course_obj')
        student_obj = validated_data.get('student_obj')
        zongbu=settings.ZONGBU
        if (course_obj.school_obj!=student_obj.school_obj) and (course_obj.school_obj.school_name!=zongbu):
            raise serializers.ValidationError({'error':'课程和学生不在同一个学校并且此课程也不在总部'})

        if relevance:
            studentcourse_obj=StudentCourseModel.objects.create(course_obj=course_obj,student_obj=student_obj)
            return studentcourse_obj
        else:
            studentcourse_obj =StudentCourseModel.objects.filter(course_obj=course_obj,
                                                             student_obj=student_obj).first()
            if studentcourse_obj:
                studentcourse_obj.delete()
            return studentcourse_obj


#这个学校里的所有章节
class SchoolDegreeSerilaizer(serializers.ModelSerializer):
    course_name=serializers.CharField(source='course_obj.course_name',read_only=True)
    class Meta:
        model=CourseDegreeModel
        fields=('id','course_name','degree_name',)









