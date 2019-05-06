from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from manager.serializers import *
from rest_framework.viewsets import mixins as M,GenericViewSet as G
from rest_framework.response import Response
from Tools import base_tool
from django.shortcuts import render
from django.db.models import Q
from UserInfo.models import UsersModel
from manager.permission_classes import *
from django.conf import settings


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 300


#省/直辖市
class ProvinceViewSet(ModelViewSet):
    permission_id=1001
    queryset = ProvinceModel.objects.get_queryset().order_by('id')
    serializer_class = ProvinceSerializer
    permission_classes = (IsManagerPermission,)


#城市/区
class CityViewSet(ModelViewSet):
    queryset = CityModel.objects.get_queryset().order_by('id')
    serializer_class = CitySerializer
    permission_classes = (IsManagerPermission,)


#学校
class SchoolViewSet(ModelViewSet):
    queryset = SchoolModel.objects.get_queryset().order_by('-updated_at')
    serializer_class = SchoolSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsManagerPermission,)
    def get_queryset(self):
        queryset=super().get_queryset()
        find=self.request.GET.get('find',None)
        if find:
            try:
                return queryset.filter(school_name__contains=find)
            except:
                raise serializers.ValidationError({'error':'检查查询参数'})
        else:
            return queryset


#课程
class CourseViewSet(G,M.ListModelMixin,M.CreateModelMixin,M.UpdateModelMixin,M.DestroyModelMixin,M.RetrieveModelMixin):
    permission_classes = (IsManagerPermission,)
    queryset =CourseModel.objects.get_queryset().order_by('-updated_at')
    serializer_class = CourseSerializer
    pagination_class = LargeResultsSetPagination
    def get_queryset(self):
        queryset=super().get_queryset()
        school_or_course=self.request.GET.get('school_or_course',None)
        if school_or_course:
            return queryset.filter(Q(school_obj__school_name__contains=school_or_course)|Q(course_name__contains=school_or_course))
        else:
            return queryset


#课程进度
class CourseDegreeViewSet(ModelViewSet):
    permission_classes = (IsManagerPermission,)
    queryset = CourseDegreeModel.objects.get_queryset().order_by('-updated_at')
    serializer_class = CourseDegreeSerializer

    def get_queryset(self):
        queryset=super().get_queryset()
        course_obj=self.request.GET.get('course_obj',None)
        if course_obj:
            try:
                return queryset.filter(course_obj__id=course_obj)
            except:
                raise serializers.ValidationError({'error':'你传输的这个参数很不合适啊.你到底传的是不是数字啊w(ﾟДﾟ)w'})
        else:
            return queryset


#管理员登陆
class ManagerLoginViewSet(G):
    permission_classes = (IsManagerPermission,)
    serializer_class = ManagerLoginSerializer

    def create(self,request):
        test=request.data.get('test')
        status=200 if test=='1' else 400
        return Response({'name':'队长'},status=status)


#权限
class PermissionViewSet(base_tool.BaseViewSet):
    permission_classes = (IsManagerPermission,)
    unique_permission_sign = (877869, '管理员登陆验证2')
    def list(self, request):
        return render(request,'permission.html',{})


#管理员登陆验证
class IsManagerLoginViewSet(base_tool.BaseViewSet):
    permission_classes = (IsManagerPermission,)
    unique_permission_sign = (87786,'管理员登陆验证')
    def list(self, request):
        user_obj=request.user
        if user_obj:
            response_data={'is_manager_login':True,'user_name':user_obj.name}
        else:
            response_data={'is_manager_login':False}
        return Response(response_data)


#总管理员对学校管理员进行操作
class SchoolManagerViewSet(ModelViewSet):
    permission_classes = (IsManagerPermission,)
    serializer_class = SchoolManagerSerializer
    pagination_class = LargeResultsSetPagination
    def get_queryset(self):
        #得到所有角色为学校管理员的家伙
        school_manager_obj=self.get_school_role_obj()
        user_objs =school_manager_obj.users_obj.all().order_by('-updated_at')

        name_or_mobile=self.request.GET.get('name_or_mobile',None)
        if name_or_mobile:
            user_objs=user_objs.filter(Q(name__contains=name_or_mobile)|
                                       Q(mobile__contains=name_or_mobile))
        return user_objs

    def get_school_role_obj(self):
        school_manager = settings.SCHOOLMANAGER_ROLE
        school_manager_obj = RolesModel.objects.filter(role_name=school_manager).first()
        if school_manager_obj:
            return school_manager_obj
        else:
            school_manager_obj=RolesModel.objects.create(role_name=school_manager)
            return school_manager_obj


#总管理员把学校与学校管理员进行绑定
class School_SchoolManagerViewSet(ModelViewSet):
    permission_classes = (IsManagerPermission,)
    serializer_class = School_SchoolManagerSerilaizer

    def get_serializer_class(self):
        serializer_class=super().get_serializer_class()
        if self.action=='list':
            return School_SchoolManagerListSerilaizer
        else:
            return serializer_class

    def get_queryset(self):
        user_id=self.request.GET.get('user_obj',None)
        if not user_id:
            school_objs =SchoolModel.objects.get_queryset().order_by('id')
        else:
            user_obj=UsersModel.objects.filter(pk=user_id).first()
            if not user_obj:errorhandler({'error':'没有找到这个用户'})
            school_objs=user_obj.schoolmodel_set.all().order_by('id')
        return school_objs

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer=serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            errorhandler({'error':serializer.errors})


class UsersRolesViewSet(ModelViewSet):
    permission_classes = (IsManagerPermission,)
    queryset = RolesModel.objects.get_queryset().order_by('id')
    serializer_class = UsersRolesSerializer













