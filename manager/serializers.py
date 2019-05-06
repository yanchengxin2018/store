from rest_framework import serializers
from main.models import ProvinceModel,CityModel,SchoolModel,CourseModel,CourseDegreeModel
from UserInfo.models import PermissionModel,RolesModel
import datetime,time
from UserInfo.serializers import CreateUserSerialzier
from Tools.base_tool import errorhandler
from django.conf import settings
from UserInfo.models import UsersModel
from Tools.user_tool import get_user_role
from error import custom_errors


#省/直辖市
class ProvinceSerializer(serializers.ModelSerializer):
    citys=serializers.SerializerMethodField(read_only=True)

    def get_citys(self,province_obj):
        city_objs=CityModel.objects.filter(province_obj=province_obj)
        citys_serializer=CitySerializer(city_objs,many=True)
        return citys_serializer.data

    class Meta:
        model=ProvinceModel
        fields=('id','province_name','citys',)


#城市/区
class CitySerializer(serializers.ModelSerializer):
    schools=serializers.SerializerMethodField(read_only=True)

    def get_schools(self,city_obj):
        school_objs=SchoolModel.objects.filter(city_obj=city_obj)
        schools_serializer=SchoolSerializer(school_objs,many=True)
        return schools_serializer.data

    class Meta:
        model=CityModel
        fields=('id','city_name','province_obj','schools',)


#学校
class SchoolSerializer(serializers.ModelSerializer):
    province_name=serializers.SerializerMethodField(read_only=True)
    city_name=serializers.SerializerMethodField(read_only=True)
    province_id=serializers.SerializerMethodField(read_only=True)
    school_manager=serializers.SerializerMethodField()

    def get_school_manager(self,school_obj):
        user_obj=school_obj.user_obj
        info='{}({})'.format(user_obj.name,user_obj.mobile) if user_obj else None
        return info

    def get_province_name(self,school_obj):
        province_obj=ProvinceModel.objects.get(citymodel__schoolmodel=school_obj)
        return province_obj.province_name

    def get_province_id(self,school_obj):
        province_obj=ProvinceModel.objects.get(citymodel__schoolmodel=school_obj)
        return province_obj.id

    def get_city_name(self,school_obj):
        city_obj=CityModel.objects.get(schoolmodel=school_obj)
        return city_obj.city_name

    class Meta:
        model=SchoolModel
        fields=('province_id','city_obj','id',
                'province_name','city_name','school_name','school_manager',)


#课程
class CourseSerializer(serializers.ModelSerializer):

    degree_count=serializers.IntegerField(help_text='输入课程的总节数',write_only=True)
    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)
    city_name=serializers.CharField(source='school_obj.city_obj.city_name',read_only=True)
    province_name=serializers.CharField(source='school_obj.city_obj.province_obj.province_name',read_only=True)
    degree_count_read=serializers.SerializerMethodField()

    def get_degree_count_read(self,course_obj):
        return CourseDegreeModel.objects.filter(course_obj=course_obj).count()

    class Meta:
        model=CourseModel
        fields=('id','province_name','city_name','school_name','course_name','degree_count',
                'created_at','updated_at','school_obj','degree_count_read',)

    def validate_degree_count(self, attrs):
        max_count=120
        if attrs>max_count or attrs<=0:
            raise serializers.ValidationError(f'这个课程有{attrs}节?请输入一个1-{max_count}的合理数字.')
        return attrs

    def create(self, validated_data):
        degree_count=validated_data.pop('degree_count')
        course_obj = super().create(validated_data)
        for i in range(degree_count):
            data={'course_obj':course_obj.id,}
            course_degree_serializer=CourseDegreeWriteOnlySerializer(data=data)
            if course_degree_serializer.is_valid():
                course_degree_serializer.save()
            else:
                print(course_degree_serializer.errors)
        return course_obj


#章节
class CourseDegreeSerializer(serializers.ModelSerializer):
    course_name=serializers.CharField(source='course_obj.course_name',read_only=True)

    class Meta:
        model=CourseDegreeModel
        fields=('id','course_name','degree_name','course_obj','remark',)

    def update(self, instance, validated_data):
        if validated_data.pop('course_obj',None):
            raise custom_errors.Status_401({'error':'更新操作不能更改course_obj'})
        return super().update(instance, validated_data)


#章节只写的(自动添加)
class CourseDegreeWriteOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model=CourseDegreeModel
        fields=('id','course_obj',)


#临时
class ManagerLoginSerializer(serializers.Serializer):
    pass


#学校管理员
class SchoolManagerSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    mobile=serializers.CharField()


    def create(self, validated_data):
        validated_data['password']='123456'
        serializer=CreateUserSerialzier(data=validated_data)

        if serializer.is_valid():
            user_obj=serializer.save()
        else:
            errorhandler({'error':serializer.errors})
            return
        school_manager_obj=self.get_school_role_obj()
        school_manager_obj.users_obj.add(user_obj)
        school_manager_obj.save()
        return user_obj

    def get_school_role_obj(self):
        school_manager = settings.SCHOOLMANAGER_ROLE
        school_manager_obj = RolesModel.objects.filter(role_name=school_manager).first()
        if school_manager_obj:
            return school_manager_obj
        else:
            school_manager_obj=RolesModel.objects.create(role_name=school_manager)
            return school_manager_obj
    class Meta:
        model=UsersModel
        fields=('id','name','mobile',)


#总管理员把学校和学校管理员进行绑定
class School_SchoolManagerSerilaizer(serializers.Serializer):
    school_obj=serializers.CharField(write_only=True)
    user_obj=serializers.CharField(write_only=True)

    def validate_user_obj(self, user_id):
        user_obj=UsersModel.objects.filter(pk=user_id).first()
        if not user_obj:raise serializers.ValidationError('没有找到这个用户')
        user_role=get_user_role(user_obj)
        if user_role != settings.SCHOOLMANAGER_ROLE:
            raise serializers.ValidationError('这个用户不是一个{}'.format(settings.SCHOOLMANAGER_ROLE))
        return user_obj

    def validate_school_obj(self, school_id):
        school_obj=SchoolModel.objects.filter(pk=school_id).first()
        if not school_obj:raise serializers.ValidationError('没有找到这个学校')
        return school_obj

    def create(self, validated_data):
        school_obj=validated_data.get('school_obj')
        user_obj=validated_data.get('user_obj')
        school_obj.user_obj=user_obj
        school_obj.save()
        return school_obj


class School_SchoolManagerListSerilaizer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    school_id=serializers.IntegerField(source='id')

    def get_user_name(self,school_obj):
        user_obj=school_obj.user_obj
        return user_obj.name if user_obj else None

    class Meta:
        model=SchoolModel
        fields=('school_id','id','school_name','user_obj','user_name',)
                # 'user_obj','user_name',)


#修改用户角色
class UsersRolesSerializer(serializers.ModelSerializer):
    names=serializers.SerializerMethodField()
    # users_obj=serializers.DjangoModelField(wirte_only=True)
    def get_names(self,role_obj):
        users_obj=role_obj.users_obj.all()
        return [user_obj.name for user_obj in users_obj]

    class Meta:
        model=RolesModel
        fields=('id','role_name','names','users_obj',)








