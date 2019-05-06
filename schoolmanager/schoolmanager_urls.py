from rest_framework.routers import DefaultRouter
from schoolmanager import views


schoolmanager_router=DefaultRouter()

schoolmanager_router.register('class',views.ClassViewSet,base_name='schoolmanager_class')
schoolmanager_router.register('classcourse',views.ClassCourseViewSet,base_name='schoolmanager_classcourse')
schoolmanager_router.register('classstudent',views.ClassStudentViewSet,base_name='schoolmanager_classstudent')
schoolmanager_router.register('classteacher',views.ClassTeacherViewSet,base_name='schoolmanager_classteacher')
schoolmanager_router.register('teacher',views.TeacherViewSet,base_name='schoolmanager_teacher')
schoolmanager_router.register('student',views.StudentViewSet,base_name='schoolmanager_student')
schoolmanager_router.register('course',views.CourseViewSet,base_name='schoolmanager_course')
schoolmanager_router.register('coursedegree',views.CourseDegreeViewSet,base_name='schoolmanager_coursedegree')
schoolmanager_router.register('school',views.SchoolViewSet,base_name='schoolmanager_school')
schoolmanager_router.register('stageclass',views.StageClassViewSet,base_name='schoolmanager_stageclass')
schoolmanager_router.register('stageschool',views.StageSchoolViewSet,base_name='schoolmanager_stageschool')
schoolmanager_router.register('studentcourse',views.StudentCourseViewSet,base_name='schoolmanager_studentcourse')
schoolmanager_router.register('schooldegreestarttime',
                              views.SchoolDegreeStartTimeViewSet,base_name='schoolmanager_schoodegreestarttime')
schoolmanager_router.register('schooldegree',views.SchoolDegreeViewSet,base_name='schoolmanager_schooldegree')








