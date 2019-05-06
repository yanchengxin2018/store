from django.db import models
from main.models import SchoolModel,CourseModel,CourseDegreeModel,StudentModel


#学校里某章节的开课时间
class SchoolDegreeStartTimeModel(models.Model):
    school_obj=models.ForeignKey(SchoolModel,on_delete=models.CASCADE,help_text='要在哪个学校设置章节的开课时间')
    degree_obj=models.ForeignKey(CourseDegreeModel,on_delete=models.CASCADE,help_text='要为哪个章节设置开课时间')
    start_time=models.DateTimeField(help_text='设置章节的开课时间')
    class Meta:
        unique_together=('school_obj','degree_obj',)
    def __str__(self):
        return '{}|{}'.format(self.degree_obj.degree_name,self.start_time)

#学生拥有的课程
class StudentCourseModel(models.Model):
    student_obj=models.ForeignKey(StudentModel,on_delete=models.CASCADE)
    course_obj=models.ForeignKey(CourseModel,on_delete=models.CASCADE)
    class Meta:
        unique_together=('student_obj','course_obj',)
















