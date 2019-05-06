from django.db import models
from UserInfo.models import UsersModel


#测试的模型
class TestModel(models.Model):
    name=models.CharField(max_length=100)


#省/直辖市
class ProvinceModel(models.Model):
    province_name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.province_name


#城市/区
class CityModel(models.Model):
    city_name=models.CharField(max_length=50,unique=True)
    province_obj=models.ForeignKey(to='ProvinceModel',on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name


#学校
class SchoolModel(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    school_name=models.CharField(max_length=50)
    city_obj=models.ForeignKey(to='CityModel',on_delete=models.CASCADE)
    user_obj=models.ForeignKey(UsersModel,on_delete=models.SET_NULL,null=True)
    class Meta:
        unique_together=('school_name','city_obj',)
    def __str__(self):
        return self.school_name


#课程
class CourseModel(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    course_name=models.CharField(max_length=50)
    school_obj=models.ForeignKey(to='SchoolModel',on_delete=models.CASCADE,)
    class Meta:
        unique_together=('school_obj','course_name',)
    def __str__(self):
        return self.course_name


#课程进度
class CourseDegreeModel(models.Model):
    created_at=models.DateTimeField(auto_now=True,help_text='创建时间')
    updated_at=models.DateTimeField(auto_now_add=True,help_text='更新时间')
    degree_name=models.CharField(max_length=50,null=True,help_text='章节的名字')
    course_obj=models.ForeignKey(to='CourseModel',on_delete=models.CASCADE)
    remark=models.TextField(null=True,help_text='章节的备注信息')
    def __str__(self):
        return '{}|{}'.format(self.course_obj,self.degree_name)


#班级
class ClassModel(models.Model):
    school_obj=models.ForeignKey(to='SchoolModel',on_delete=models.CASCADE)
    class_name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.class_name
    class Meta:
        unique_together=('school_obj','class_name',)


#班级里的课程
class ClassCourseModel(models.Model):
    class_obj=models.ForeignKey(to='ClassModel',on_delete=models.CASCADE)
    course_obj=models.ForeignKey(to='CourseModel',on_delete=models.CASCADE)
    class Meta:
        unique_together=('class_obj','course_obj',)


#班级里的学生
class ClassStudentModel(models.Model):
    user_obj=models.OneToOneField(UsersModel,on_delete=models.CASCADE)
    class_obj=models.ForeignKey(ClassModel,on_delete=models.CASCADE)


#老师
class TeacherModel(models.Model):
    user_obj=models.OneToOneField(UsersModel,on_delete=models.CASCADE)
    class_obj=models.ManyToManyField(ClassModel)
    school_obj=models.ForeignKey(SchoolModel,on_delete=models.CASCADE)


#学生
class StudentModel(models.Model):
    user_obj=models.OneToOneField(UsersModel,on_delete=models.CASCADE)
    class_obj=models.ForeignKey(ClassModel,on_delete=models.CASCADE,null=True)
    school_obj=models.ForeignKey(SchoolModel,on_delete=models.CASCADE)
    def __str__(self):
        return '{}|[{}]'.format(self.user_obj.name,self.id)


#学生的信息/这个表记录了学生的学习状况
class StudentInfoModel(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    created_data_at=models.DateField(auto_now=True,help_text='创建日期')
    red_card=models.IntegerField(default=None,null=True)
    blue_card=models.IntegerField(default=None,null=True)
    yellow_card=models.IntegerField(default=None,null=True)
    course_comment=models.TextField(default="",null=True)
    stage_comment=models.TextField(default=None,null=True)
    study=models.BooleanField(default=True)
    student_obj=models.ForeignKey(to='StudentModel',on_delete=models.CASCADE)

    class_name_log=models.CharField(max_length=20,null=True,help_text='记录这条信息时,学生所在的班级')
    degree_name_log=models.CharField(max_length=20,null=True,help_text='记录这条信息时,学生的课程章节')
    study_time_log=models.DateTimeField(null=True)
    course_obj_log=models.ForeignKey(CourseModel,on_delete=models.SET_NULL,null=True)





    class Meta:
        unique_together=('created_data_at','student_obj',)


#班级阶段性评测的时间表
class StageClassModel(models.Model):
    comment_time=models.DateField(help_text='提交一个时间,在这天时,这个班级的老师会被要求提交阶段性评价')
    class_obj=models.ForeignKey(to='ClassModel',on_delete=models.CASCADE,
                                help_text='当comment_time这个时间点到达,这个班级的老师会被要求提交阶段性评价')
    class Meta:
        unique_together=('class_obj','comment_time',)


#学校阶段性评测的时间表
class StageSchoolModel(models.Model):
    comment_time=models.DateField(help_text='提交一个时间,在这天时,这个学校的老师会被要求提交阶段性评价')
    school_obj=models.ForeignKey(to='SchoolModel',on_delete=models.CASCADE,
                                help_text='当comment_time这个时间点到达,这个学校的老师会被要求提交阶段性评价')

    class Meta:
        unique_together=('school_obj','comment_time',)


#班级通知表
class ClassNoticeModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True,help_text='创建时间')
    class_obj=models.ForeignKey(to='ClassModel',on_delete=models.CASCADE,help_text='要发布通知的班级')
    notice=models.TextField(help_text='发布通知内容')
    send_start_date=models.DateTimeField(help_text='通知的开始时间')
    send_end_date=models.DateTimeField(help_text='通知的结束时间')



    def __str__(self):
        info='{}--{}|{}|{}'.format(self.send_start_date,self.send_end_date,self.class_obj.class_name,self.notice)
        return info







