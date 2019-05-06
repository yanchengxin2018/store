from rest_framework.viewsets import ModelViewSet
from schoolmanager.serializers import *
from main.models import ClassStudentModel,TeacherModel,SchoolModel,ClassModel,ClassCourseModel
from Tools.base_tool import errorhandler
from rest_framework.response import Response
from django.db.models import Q
from schoolmanager.permissions import *
from UserInfo.models import RolesModel
from rest_framework.viewsets import mixins as M,GenericViewSet as G
from Tools.base_tool import LargeResultsSetPagination
from Tools.schoolmanager_tool import *
from Tools.schoolmanager_tool import school_obj_and_school_manager
from main.models import StageClassModel,StageSchoolModel
from schoolmanager.models import SchoolDegreeStartTimeModel,StudentCourseModel
from schoolmanager.serializers import SchoolDegreeStartTimeSerializer,StudentCourseSerializer
from .serializers import StudentCourseWriteOnlySerializer
from schoolmanager.serializers import SchoolDegreeSerilaizer


#查看学校
class SchoolViewSet(G,M.ListModelMixin,M.RetrieveModelMixin,M.UpdateModelMixin):
    permission_classes = (IsSchoolManagerPermission,)
    serializer_class = SchoolSerializer
    def get_queryset(self):
        schools_obj=SchoolModel.objects.filter(user_obj=self.request.user).order_by('id')
        return schools_obj


#班级
class ClassViewSet(ModelViewSet):
    serializer_class = ClassSerializer
    queryset = ClassModel.objects.get_queryset().order_by('-updated_at')
    pagination_class = LargeResultsSetPagination
    def get_queryset(self):

        query_set=super().get_queryset()
        class_or_school_name=self.request.GET.get('class_or_school_name',None)
        if not class_or_school_name:return query_set
        query_set=query_set.filter(Q(class_name__contains=class_or_school_name)|
                         Q(school_obj__school_name__contains=class_or_school_name))
        return query_set.order_by('id')


#老师管理
class TeacherViewSet(ModelViewSet):
    permission_classes =(IsSchoolManagerPermission,)
    serializer_class = TeacherSerializer

    def get_queryset(self):
        teachers_obj=TeacherModel.objects.filter(school_obj__user_obj=self.request.user)
        if not teachers_obj:return []
        user_ids=[teacher_obj.user_obj.id for teacher_obj in teachers_obj]
        users_obj=UsersModel.objects.filter(id__in=user_ids)
        teacher_name=self.request.GET.get('teacher_name',None)
        if teacher_name:
            users_obj =users_obj.filter(name__contains=teacher_name)
        return users_obj.order_by('id')


#学生管理
class StudentViewSet(ModelViewSet):
    permission_classes =(IsSchoolManagerPermission,)
    serializer_class = StudentSerializer

    def get_queryset(self):
        students_obj=StudentModel.objects.filter(school_obj__user_obj=self.request.user)
        if not students_obj:return []
        user_ids=[student_obj.user_obj.id for student_obj in students_obj]
        users_obj=UsersModel.objects.filter(id__in=user_ids)
        student_name=self.request.GET.get('student_name',None)
        if student_name:
            users_obj =users_obj.filter(name__contains=student_name)
        return users_obj.order_by('id')


#本校的课程管理
class CourseViewSet(ModelViewSet):
    permission_classes = (IsSchoolManagerPermission,)
    queryset = CourseModel.objects.get_queryset().order_by('-updated_at')
    serializer_class = CourseSerializer
    # pagination_class = LargeResultsSetPagination
    pagination_class = LargeResultsSetPagination
    def get_queryset(self):
        user_obj=self.request.user
        schools_obj=SchoolModel.objects.filter(user_obj=user_obj)
        courses_obj=CourseModel.objects.filter(school_obj__in=schools_obj)
        school_or_course_name=self.request.GET.get('school_or_course_name',None)
        if school_or_course_name:
            try:
                courses_obj=courses_obj.filter(Q(school_obj__school_name__contains=school_or_course_name)|
                                           Q(course_name__contains=school_or_course_name))
            except:
                raise serializers.ValidationError({'error':'检查school_or_course_name参数'})
        return courses_obj.order_by('-updated_at')


#章节
class CourseDegreeViewSet(ModelViewSet):
    permission_classes = (IsSchoolManagerPermission,IsSchoolManageAndOwnerPermission,)
    queryset = CourseDegreeModel.objects.get_queryset().order_by('id')
    serializer_class = CourseDegreeSerializer
    def get_serializer_class(self):
        if self.action=='update':
            return DegreeUpdateSerialzier
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        #所有与这个管理员相关的课程
        zongbu=settings.ZONGBU
        schools_obj=SchoolModel.objects.filter(user_obj=self.request.user)
        if self.action=='list':
            degree_obj=CourseDegreeModel.objects.filter(Q(course_obj__school_obj__in=schools_obj)|
                                                        Q(course_obj__school_obj__school_name=zongbu))
        else:
            degree_obj = CourseDegreeModel.objects.filter(course_obj__school_obj__in=schools_obj)
        #通过条件进行筛选
        course_id = self.request.GET.get('course_obj', None)
        if course_id:
            degree_obj=degree_obj.filter(course_obj__id=course_id)
        degree_name=self.request.GET.get('degree_name',None)
        return degree_obj.order_by('id')


#绑定班级和老师
class ClassTeacherViewSet(G,M.ListModelMixin,M.CreateModelMixin):
    permission_classes = (IsSchoolManagerPermission,)
    serializer_class = ClassTeacherSerializer
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        serializer_class=super().get_serializer_class()
        if self.action=='list':
            return serializer_class
        elif self.action=='create':
            return CreateClassTeacherSerializer

    def get_queryset(self):
        #得到这个班级所属学校的所有老师
        class_id=self.request.GET.get('class_obj',None)
        if not class_id:raise serializers.ValidationError({'error':'class_obj参数是必选的'})
        try:
            class_obj=ClassModel.objects.filter(pk=class_id).first()

        except:
            raise serializers.ValidationError({'error':'检查class_obj参数是不是一个整数'})
        if not class_obj:raise serializers.ValidationError({'error':'没有找到这个班级'})
        school_obj=class_obj.school_obj
        if not school_obj:raise serializers.ValidationError({'error':'这个班级不属于任何学校'})



        teachers_obj=get_teacher_of_school_manager(self.request.user)
        teacher_name=self.request.GET.get('teacher_name',None)
        if teacher_name:
            teachers_obj=teachers_obj.filter(user_obj__name__contains=teacher_name)
        teachers_obj =teachers_obj.filter(school_obj=school_obj)
        return teachers_obj.order_by('id')


#绑定班级和课程
class ClassCourseViewSet(G,M.ListModelMixin,M.CreateModelMixin):
    permission_classes = (IsSchoolManagerPermission,)
    pagination_class = LargeResultsSetPagination
    def get_serializer_class(self):
        if self.action=='list':
            return ClassCourseSerializer
        elif self.action=='create':
            return CreateClassCourseSerializer

    def get_queryset(self):
        #学校管理员的所有课程与班级所在学校的所有课程的交集
        #筛选为课程所在学校的所有课程
        class_id=self.request.GET.get('class_obj')
        if not class_id:raise serializers.ValidationError({'error':'必须使用class_obj参数'})
        try:
            class_obj=ClassModel.objects.filter(pk=class_id).first()
        except:
            raise serializers.ValidationError({'error':'检查class_obj参数'})
        if not class_obj:raise serializers.ValidationError({'error':'没有找到这个班级'})
        school_obj=class_obj.school_obj
        if not school_obj:raise serializers.ValidationError({'error':'这个班级不属于任何学校'})
        if not school_obj_and_school_manager(school_obj,self.request.user):
            raise serializers.ValidationError({'error':'当前账户没有权限操作这个班级'})
        courses_obj=CourseModel.objects.filter(Q(school_obj=school_obj)|
                                               Q(school_obj__school_name__contains='总部'))
        #关键字搜索
        course_name=self.request.GET.get('course_name',None)
        if course_name:
            courses_obj=courses_obj.filter(course_name__contains=course_name)
        return courses_obj.order_by('id')


#绑定班级和学生
class ClassStudentViewSet(G,M.ListModelMixin,M.CreateModelMixin):
    permission_classes = (IsSchoolManagerPermission,)
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.action=='list':
            return ClassStudentSerializer
        elif self.action=='create':
            return CreateClassStudentSerializer

    def get_queryset(self):
        #筛选为班级所在学校的所有学生
        class_id=self.request.GET.get('class_obj')
        if not class_id:raise serializers.ValidationError({'error':'必须使用class_obj参数'})
        try:
            class_obj=ClassModel.objects.filter(pk=class_id).first()
        except:
            raise serializers.ValidationError({'error':'检查class_obj参数'})
        if not class_obj:raise serializers.ValidationError({'error':'没有找到这个班级'})
        school_obj=class_obj.school_obj
        if not school_obj:raise serializers.ValidationError({'error':'这个班级不属于任何学校'})
        if not school_obj_and_school_manager(school_obj,self.request.user):
            raise serializers.ValidationError({'error':'当前账户没有权限操作这个班级'})

        students_obj=StudentModel.objects.filter(school_obj=school_obj)

        #关键字搜索
        student_name=self.request.GET.get('student_name',None)
        if student_name:
            students_obj=students_obj.filter(user_obj__name__contains=student_name)
        return students_obj.order_by('id')


#为班级的阶段性评测设置一个时间点
class StageClassViewSet(ModelViewSet):
    '''
        为班级的阶段性评测设置一个时间点
    '''
    permission_classes = (IsSchoolManagerPermission,)
    queryset = StageClassModel.objects.all().order_by('-comment_time')
    serializer_class = StageClassSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset=super().get_queryset()
        class_id=self.request.GET.get('class_obj',None)
        if class_id:
            queryset=queryset.filter(class_obj__id=class_id)
        return queryset


# 为学校的阶段性评测设置一个时间点
class StageSchoolViewSet(ModelViewSet):
    '''
        为学校的阶段性评测设置一个时间点
    '''
    permission_classes = (IsSchoolManagerPermission,)
    queryset = StageSchoolModel.objects.all().order_by('-comment_time')
    serializer_class = StageSchoolSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset=super().get_queryset()
        school_id=self.request.GET.get('school_obj',None)
        if self.action=='list':
            if not school_id:raise custom_errors.Status_400({'error':'传输一个school_obj'})
        if school_id:
            try:
                queryset=queryset.filter(school_obj__id=school_id)
            except:
                raise custom_errors.Status_400({'error':'school_obj不能被理解'})
        return queryset


# 学校管理员编辑本校章节的开课时间
class SchoolDegreeStartTimeViewSet(ModelViewSet):
    '''
    学校管理员编辑本校课程的开课时间
    '''
    permission_classes = (IsSchoolManagerPermission,)
    serializer_class = SchoolDegreeStartTimeSerializer
    pagination_class = LargeResultsSetPagination
    def get_queryset(self):
        schools_obj=SchoolModel.objects.filter(user_obj=self.request.user)
        schoolcoursestarttime_obj=SchoolDegreeStartTimeModel.objects.filter(school_obj__in=schools_obj)
        school_id=self.request.GET.get('school_obj',None)
        if school_id:
            schoolcoursestarttime_obj=schoolcoursestarttime_obj.filter(school_obj__id=school_id)
        degree_name=self.request.GET.get('degree_name',None)
        if degree_name:
            schoolcoursestarttime_obj = schoolcoursestarttime_obj.filter(degree_obj__degree_name__contains=degree_name)
        return schoolcoursestarttime_obj.order_by('id')


#绑定学生课程
class StudentCourseViewSet(ModelViewSet):
    serializer_class = StudentCourseSerializer
    permission_classes = (IsSchoolManagerPermission,)
    pagination_class = LargeResultsSetPagination
    def get_serializer_class(self):
        if self.action=='list':
            return super().get_serializer_class()
        else:

            return StudentCourseWriteOnlySerializer

    def get_queryset(self):
        zongbu=settings.ZONGBU
        queryset =CourseModel.objects.filter(Q(school_obj__user_obj=self.request.user)|
                                             Q(school_obj__school_name=zongbu))
        student_id=self.request.GET.get('student_obj',None)
        if not student_id:
                raise custom_errors.Status_400({'error':'student_obj参数是必须的'})
        course_name=self.request.GET.get('course_name',None)
        if course_name:
            queryset=queryset.filter(course_name__contains=course_name)
        return queryset.order_by('-updated_at')


#这个学校里所有的章节
class SchoolDegreeViewSet(G,M.ListModelMixin):

    serializer_class = SchoolDegreeSerilaizer
    queryset = CourseDegreeModel.objects.all().order_by('id')

    def get_queryset(self):
        school_obj=self.get_school_obj()
        queryset = CourseDegreeModel.objects.filter(course_obj__school_obj=school_obj)
        course_name_or_degree_name=self.request.GET.get('course_name_or_degree_name',None)
        if course_name_or_degree_name:
            queryset=queryset.filter(Q(course_obj__course_name__contains=course_name_or_degree_name)|
                                     Q(degree_name__contains=course_name_or_degree_name))
        return queryset.order_by('id')

    def get_school_obj(self):
        school_id = self.request.GET.get('school_obj', None)
        if not school_id:raise custom_errors.Status_400({'error':'school_obj参数是必须的'})
        try:
            school_obj=SchoolModel.objects.filter(pk=school_id).first()
        except:
            raise custom_errors.Status_400({'error':'无法识别的参数school_obj'})
        if not school_obj:raise custom_errors.Status_404({'error':'没有找到这个学校'})
        if school_obj.user_obj!=self.request.user:
            raise custom_errors.Status_401({'error':'没有权限操作这所学校'})
        return school_obj



