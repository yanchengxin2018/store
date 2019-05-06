from teacher.serializers import StudentInfoSerializer
import datetime
from main.models import StudentInfoModel
from teacher.tools import get_stage_status,get_student_edit_status
from main.models import TeacherModel,StudentModel

#得到一条今日的学生信息
def get_today_student_info(student_obj):
    # 得到学生的obj和今天的时间
    created_data_obj = datetime.date.today()
    # 通过这两个参数搜索这条学生信息的记录
    student_info_obj = StudentInfoModel.objects.filter(student_obj=student_obj.id,
                                                       created_data_at=created_data_obj).first()
    # 如果搜索到了这个学生今天的记录
    serializer_class = StudentInfoSerializer
    serializer_obj = serializer_class(student_info_obj)
    data = serializer_obj.data
    if student_info_obj:
        stage_status = get_stage_status(student_obj)
        edit_status = get_student_edit_status(student_obj)
        data['student_obj'] = student_obj.id
        data['stage_status'] = stage_status
        data['edit_status'] = edit_status
        data['name'] = student_obj.user_obj.name
        data['class_obj'] = student_obj.class_obj.id
        data['class_name'] = student_obj.class_obj.class_name
        data['school_name'] = student_obj.school_obj.school_name
        return data
    else:
        stage_status = get_stage_status(student_obj)
        edit_status = get_student_edit_status(student_obj)
        data['student_obj']=student_obj.id
        data['stage_status'] = stage_status
        data['edit_status'] = edit_status
        data['name'] = student_obj.user_obj.name
        data['class_obj'] = student_obj.class_obj.id
        data['class_name'] = student_obj.class_obj.class_name
        data['school_name'] = student_obj.school_obj.school_name
        return data




#这个老师今日的任务状态
def get_edit_status(user_obj):
        #只要有一个学生还未编辑完成,那么编辑状态是True,老师应该继续编辑
        teacher_obj=TeacherModel.objects.filter(user_obj=user_obj).first()
        classes_obj=teacher_obj.class_obj.all()
        students_obj=StudentModel.objects.filter(class_obj__in=classes_obj)
        for student_obj in students_obj:
            if get_student_edit_status(student_obj):
                return True
        return False




















