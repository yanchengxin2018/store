from rest_framework.viewsets import GenericViewSet as G,mixins as M
from main.models import ClassNoticeModel,StudentModel
from student.serializers import StudentNoticeSerializer,StudentSerializer
from student.permissions import IsStudentPermission
import datetime
from django.contrib.auth import get_user_model
from error import custom_errors
from main.models import StudentInfoModel
from student.serializers import StudentInfoSerializer,DegreeSerializer
from rest_framework.response import Response
from main.models import CourseModel
from schoolmanager.models import SchoolDegreeStartTimeModel
UserModel=get_user_model()


#这位同学的通知
class StudentNoticeViewSet(G,M.ListModelMixin):
    '''
    在这里对学生发送班级通知
    '''
    permission_classes = (IsStudentPermission,)
    queryset = ClassNoticeModel.objects.all().order_by('id')
    serializer_class = StudentNoticeSerializer

    def get_queryset(self):
        user_obj=self.request.user
        student_obj=StudentModel.objects.filter(user_obj=user_obj).first()
        class_obj=student_obj.class_obj
        now=datetime.datetime.now()
        classnotices_obj=ClassNoticeModel.objects.filter(class_obj=class_obj,send_start_date__lt=now)
        return classnotices_obj.order_by('-send_start_date')


#这位同学的个人信息
class MyInfoViewSet(G,M.UpdateModelMixin,M.RetrieveModelMixin):

    permission_classes = (IsStudentPermission,)
    serializer_class = StudentSerializer

    def get_queryset(self):
        users_obj=UserModel.objects.filter(id=self.request.user.id)
        return users_obj.order_by('id')

    def get_object(self):
        self.kwargs['pk']=self.request.user.id
        return super().get_object()

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        kwargs['partial']=True
        return super().update(request, *args, **kwargs)


#学习记录
class StudentLogInfoViewSet(G,M.ListModelMixin,M.RetrieveModelMixin):
    serializer_class = StudentInfoSerializer
    permission_classes = (IsStudentPermission,)

    def get_queryset(self):
        student_obj=StudentModel.objects.filter(user_obj=self.request.user).first()
        student_infos_obj=StudentInfoModel.objects.filter(student_obj=student_obj)
        course_obj=self.request.GET.get('course_obj',None)
        if course_obj:
            student_infos_obj=student_infos_obj.filter(course_obj_log__id=course_obj)
        else:
            raise custom_errors.Status_400({'error':'提交一个课程的id--course_obj'})
        return student_infos_obj.order_by('-updated_at')


#当前的课程及章节信息
class NowCourseViewSet(G,M.ListModelMixin):
    serializer_class = DegreeSerializer
    def list(self, request, *args, **kwargs):
        #查找课程
        course_obj=self.find_course_obj()
        #查找最近的章节
        previous_degree_obj=self.find_previous_degree_obj(course_obj)
        next_degree_obj=self.find_next_degree_obj(course_obj)
        #把章节进行序列化
        serializer_class=self.get_serializer_class()
        previous_serializer=serializer_class(previous_degree_obj,
            context={'view': self}) if previous_degree_obj else None
        next_serializer=serializer_class(next_degree_obj,
            context={'view': self}) if next_degree_obj else None
        #包装成新的结构
        data={
            'previous_degree_info':previous_serializer.data if previous_serializer else None,
            'next_degree_info':next_serializer.data  if next_serializer else None
        }
        #返回
        return Response(data)

    # 查找课程
    def find_course_obj(self):

        course_obj=CourseModel.objects.filter(studentcoursemodel__student_obj__user_obj=self.request.user).first()
        if not course_obj:raise custom_errors.Status_403({'error':'当前用户不拥有任何课程'})
        return course_obj

    #得到较早的章节
    def find_previous_degree_obj(self,course_obj):
        now=datetime.datetime.now()
        degree_start_time_obj=SchoolDegreeStartTimeModel.objects.filter(degree_obj__course_obj=course_obj,
            start_time__lt=now).order_by('-start_time').first()
        if not degree_start_time_obj:return None
        degree_obj=degree_start_time_obj.degree_obj
        return degree_obj

    #得到较晚的章节
    def find_next_degree_obj(self,course_obj):
        now=datetime.datetime.now()
        degree_start_time_obj=SchoolDegreeStartTimeModel.objects.filter(degree_obj__course_obj=course_obj,
            start_time__gt=now).order_by('start_time').first()
        if not degree_start_time_obj:return None
        degree_obj=degree_start_time_obj.degree_obj
        return degree_obj











