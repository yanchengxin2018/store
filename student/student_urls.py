from rest_framework.routers import DefaultRouter
from student import views


student_router=DefaultRouter()
student_router.register(r'studentnotice',views.StudentNoticeViewSet,base_name='studentnotice')
student_router.register(r'myinfo',views.MyInfoViewSet,base_name='myinfo')
student_router.register(r'student_log_info',views.StudentLogInfoViewSet,base_name='student_log_info')
student_router.register(r'now_course_info',views.NowCourseViewSet,base_name='now_course_info')



























