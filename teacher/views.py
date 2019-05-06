from rest_framework.viewsets import mixins as M,GenericViewSet as G,ModelViewSet
from teacher.serializers import *
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from teacher.permissions import IsTeacherPermission,IsTeacherAndReadSelfOnlyPermission
from main.models import StudentModel
from Tools.teacher_tool import *
from django.db.models import Q
from error import custom_errors
import datetime
from teacher.tools import get_student_edit_status,get_stage_status
from teacher.tools_2 import get_today_student_info
from main.models import StudentModel,StudentInfoModel


#查询登陆老师的个人信息
class MyInfoViewSet(G,M.ListModelMixin,M.CreateModelMixin):
    serializer_class = MyInfoSerializer
    permission_classes = (IsTeacherAndReadSelfOnlyPermission,)
    def get_serializer_class(self):
        if self.action=='list':
            return MyInfoReadOnlySerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        user_model=get_user_model()
        user=self.request.user
        user_obj=user_model.objects.filter(pk=user.id)
        return user_obj

    def list(self, request, *args, **kwargs):
        serializer_class=self.get_serializer_class()
        serializer=serializer_class(request.user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer=serializer_class(request.user,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)


#班级
class ClassViewSet(G,M.ListModelMixin):
    permission_classes = (IsTeacherPermission,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        user_obj=self.request.user
        teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj:raise serializers.ValidationError({'error':'没有找到这个老师'})
        classes_obj=teacher_obj.class_obj
        if not classes_obj:return []
        classes_obj =classes_obj.all()
        return classes_obj.order_by('id')

    def list(self, request, *args, **kwargs):
        response=super().list(request, *args, **kwargs)
        response.data['edit']=self.get_edit_status()
        return response

    def get_edit_status(self):
        #只要有一个学生还未编辑完成,那么编辑状态是True,老师应该继续编辑
        teacher_obj=TeacherModel.objects.filter(user_obj=self.request.user).first()
        classes_obj=teacher_obj.class_obj.all()
        students_obj=StudentModel.objects.filter(class_obj__in=classes_obj)
        for student_obj in students_obj:
            if get_student_edit_status(student_obj):
                return True
        return False


#学生
class StudentViewSet(G,M.ListModelMixin):
    # permission_classes = (IsTeacherPermission,)
    # serializer_class = StudentSerializer
    #
    # def get_queryset(self):
    #     user_obj=self.request.user
    #     teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
    #     if not teacher_obj:raise custom_errors.Status_404({'error':'没有找到这个老师'})
    #     classes_obj=teacher_obj.class_obj.all()
    #     students_obj=StudentModel.objects.filter(class_obj__in=classes_obj)
    #     class_or_student_name=self.request.GET.get('class_or_student_name',None)
    #     if class_or_student_name:
    #         try:
    #             students_obj=students_obj.filter(Q(class_obj__class_name__contains=class_or_student_name)|
    #                             Q(user_obj__name__contains=class_or_student_name))
    #         except:
    #             raise custom_errors.Status_400({'error':'检查class_or_student_name参数'})
    #     return students_obj.order_by('id')

    queryset = StudentInfoModel.objects.all().order_by('id')
    serializer_class = StudentInfoSerializer

    def get_queryset(self):
        if self.action=='list':
            user_obj = self.request.user
            teacher_obj = TeacherModel.objects.filter(user_obj=user_obj).first()
            if not teacher_obj: raise custom_errors.Status_404({'error': '没有找到这个老师'})
            classes_obj = teacher_obj.class_obj.all()
            students_obj = StudentModel.objects.filter(class_obj__in=classes_obj)
            class_or_student_name = self.request.GET.get('class_or_student_name', None)
            if class_or_student_name:
                try:
                    students_obj = students_obj.filter(Q(class_obj__class_name__contains=class_or_student_name) |
                                                       Q(user_obj__name__contains=class_or_student_name))
                except:
                    raise custom_errors.Status_400({'error': '检查class_or_student_name参数'})
            return students_obj.order_by('id')
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        if self.action=='list':
            return StudentSerializer
        else:
            return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        datas=super().list(request, *args, **kwargs).data
        from teacher.tools_2 import get_today_student_info
        student_infos=[]
        for student_obj in self.get_queryset():
            data=get_today_student_info(student_obj)
            student_infos.append(data)
        datas['results']=student_infos
        response_obj=Response(datas)
        from teacher.tools_2 import get_edit_status
        response_obj.data['students_edit_status']=get_edit_status(request.user)
        return response_obj


#学生今日学习状况
class StudentInfoViewSet(G,M.RetrieveModelMixin,M.UpdateModelMixin,M.ListModelMixin):
    '''
    学生今日的学习状况
    '''
    queryset = StudentInfoModel.objects.all().order_by('id')
    serializer_class = StudentInfoSerializer
    permission_classes = (IsTeacherPermission,)

    def get_queryset(self):
        user_obj = self.request.user
        teacher_obj = TeacherModel.objects.filter(user_obj=user_obj).first()
        if not teacher_obj: raise custom_errors.Status_404({'error': '没有找到这个老师'})
        classes_obj = teacher_obj.class_obj.all()
        students_obj = StudentModel.objects.filter(class_obj__in=classes_obj)
        class_or_student_name = self.request.GET.get('class_or_student_name', None)
        if class_or_student_name:
            try:
                students_obj = students_obj.filter(Q(class_obj__class_name__contains=class_or_student_name) |
                                                   Q(user_obj__name__contains=class_or_student_name))
            except:
                raise custom_errors.Status_400({'error': '检查class_or_student_name参数'})
        today=datetime.date.today()
        today_start=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        one_day=datetime.timedelta(days=1)
        today_end=today_start+one_day
        students_obj=students_obj.filter(
            studentcoursemodel__course_obj__coursedegreemodel__schooldegreestarttimemodel__start_time__gt=today_start,
            studentcoursemodel__course_obj__coursedegreemodel__schooldegreestarttimemodel__start_time__lt=today_end,
        )
        return students_obj.distinct().order_by('id')

    def get_serializer_class(self):
        if self.action=='list':
            return StudentSerializer
        else:
            return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        datas=super().list(request, *args, **kwargs).data
        student_infos=[]
        for student_obj in self.get_queryset():
            data=get_today_student_info(student_obj)
            student_infos.append(data)
        datas['results']=student_infos
        return Response(datas)

    #得到学生实例
    def get_student_obj(self,kwargs):
        student_id=self.kwargs.get('pk',None)
        # if not student_id:raise serializers.ValidationError({'error':'要查看学生信息请提供student_obj参数'})
        try:
            student_obj=StudentModel.objects.filter(pk=student_id).first()
        except:
            raise custom_errors.Status_400({'error':'检查student_obj参数'})
        if not student_obj:raise custom_errors.Status_404({'error':'没有查找到这个学生'})
        if not student_obj_and_teacher_obj(student_obj,self.request.user):
            raise custom_errors.Status_401({'error':'当前用户没有权限操作这个学生'})
        return student_obj

    #得到或者创建一条学生信息记录
    def get_student_info_obj(self,student_obj):
        today=datetime.date.today()
        studentinfo_obj=StudentInfoModel.objects.filter(student_obj=student_obj,created_data_at=today).first()
        if not studentinfo_obj:
            studentinfo_obj=StudentInfoModel.objects.create(student_obj=student_obj,created_data_at=today)
        return studentinfo_obj

    #索引
    def retrieve(self, request, *args, **kwargs):
        student_obj=self.get_student_obj(kwargs)
        data = get_today_student_info(student_obj)
        return Response(data)

    #更新
    def update(self, request, *args, **kwargs):
        student_obj=self.get_student_obj(kwargs)
        student_info_obj=self.get_student_info_obj(student_obj)
        serializer_class=self.get_serializer_class()
        course_comment = request.data.get('course_comment', None)
        if not course_comment:
            try:
                request.data._mutable=True
            except:
                pass
            request.data['course_comment'] = None
            try:
                request.data._mutable = False
            except:
                pass
        serializer=serializer_class(student_info_obj,request.data,partial=True)
        if serializer.is_valid():
            student_info_obj=serializer.save()
            data=get_today_student_info(student_info_obj.student_obj)
            return Response(data)
        else:
            raise serializers.ValidationError(serializer.errors)


#发布通知
class ClassNoticeViewSet(ModelViewSet):
    '''
    这个接口用于管理一个班级里的通知
    '''
    permission_classes = (IsTeacherPermission,)
    serializer_class = ClassNoticeSerialzier

    def get_queryset(self):
        teacher_obj=TeacherModel.objects.filter(user_obj=self.request.user).first()
        classes_obj=teacher_obj.class_obj.all()
        classnotice_obj=ClassNoticeModel.objects.filter(class_obj__in=classes_obj)
        class_id=self.request.GET.get('class_obj',None)
        if class_id:
            try:
                classnotice_obj=classnotice_obj.filter(class_obj__id=class_id)
            except:
                raise custom_errors.Status_400({'error':'服务器无法理解参数class_obj'})
        return classnotice_obj.order_by('-send_start_date')























