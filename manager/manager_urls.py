from rest_framework.routers import DefaultRouter
from manager import views as manager_views


manager_router=DefaultRouter()
manager_router.register('Provinces',manager_views.ProvinceViewSet,base_name='Provinces')
manager_router.register('Citys',manager_views.CityViewSet,base_name='Citys')
manager_router.register('Schools',manager_views.SchoolViewSet,base_name='Schools')
manager_router.register('Courses',manager_views.CourseViewSet,base_name='Courses')
manager_router.register('CourseDegrees',manager_views.CourseDegreeViewSet,base_name='CourseDegrees')
manager_router.register('ManagerLogin',manager_views.ManagerLoginViewSet,base_name='ManagerLogin')
manager_router.register('Permission',manager_views.PermissionViewSet,base_name='Permission')
manager_router.register('IsManagerLogin',manager_views.IsManagerLoginViewSet,base_name='IsManagerLogin')
manager_router.register('SchoolManager',manager_views.SchoolManagerViewSet,base_name='SchoolManager')
manager_router.register('School_SchoolManager',manager_views.School_SchoolManagerViewSet,
                        base_name='School_SchoolManager')
manager_router.register('UsersRoles',manager_views.UsersRolesViewSet,base_name='UsersRoles')




