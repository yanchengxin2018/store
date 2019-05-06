from rest_framework.routers import DefaultRouter
from teacher import views


teacher_router=DefaultRouter()

teacher_router.register('myinfo',views.MyInfoViewSet,base_name='teacher_myinfo')
teacher_router.register('class',views.ClassViewSet,base_name='teacher_class')
teacher_router.register('student',views.StudentViewSet,base_name='teacher_student')
teacher_router.register('student_info',views.StudentInfoViewSet,base_name='teacher_student_info')
teacher_router.register('classnotice',views.ClassNoticeViewSet,base_name='teacher_classnotice')









