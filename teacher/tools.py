from main.models import StudentInfoModel,StageClassModel,StageSchoolModel
import datetime


#得到这个学生的编辑状态
def get_student_edit_status(student_obj):

    #1.检测今天的学生的上课信息是不是被创建
    today = datetime.date.today()
    student_info_obj=StudentInfoModel.objects.filter(created_data_at=today, student_obj=student_obj).first()
    # 如果不存在今天的学生信息,那么编辑状态是True,老师应该继续编辑
    if not student_info_obj:
        return True

    #2.学生的上课信息的所有字段是不是被全部编辑了
    fields=['red_card','blue_card','yellow_card','course_comment',]
    for field in fields:
        field_edit_status=getattr(student_info_obj,field)
        #如果这个字段还没有编辑,那么编辑状态是True,老师应该继续编辑
        if field_edit_status is None:
            return True
        # print('这个字段{}已经编辑'.format(field))
        # print(field)

    #3.班级的阶段性评测是不是在今天
    stage_class=StageClassModel.objects.filter(comment_time=today,class_obj=student_obj.class_obj).first()
    #如果今天存在班级的阶段性评测,并且阶段性评测还没有填写,那么编辑状态是True,老师应该继续编辑
    if stage_class and not student_info_obj.stage_comment:
        return True

    # 4.学校的阶段性评测是不是在今天
    stage_school =StageSchoolModel.objects.filter(comment_time=today,school_obj=student_obj.school_obj).first()
    #如果今天存在学校的阶段性评测,并且阶段性评测还没有填写,那么编辑状态是True,老师应该继续编辑
    if stage_school and not student_info_obj.stage_comment:
        return True

    #5.如果所有单元都不再要求编辑,那么终于可以返回False,老师不必继续编辑了
    return False


#这个学生今天是不是有阶段性测评
def get_stage_status(student_obj):
    # if not student_obj:return
    today=datetime.date.today()
    #班级的阶段性评测是不是在今天
    stage_class=StageClassModel.objects.filter(comment_time=today,class_obj=student_obj.class_obj).first()
    if stage_class:
        return True
    # 学校的阶段性评测是不是在今天
    stage_school =StageSchoolModel.objects.filter(comment_time=today,school_obj=student_obj.school_obj).first()
    if stage_school:
        return True
    #如果班级和学校的阶段性测评都不在今天,那么返回False
    return False













