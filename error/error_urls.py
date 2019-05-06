from rest_framework.routers import DefaultRouter
from error import views


error_router=DefaultRouter()
error_router.register(r'exceptionlog',views.ExceptionLogViewSet,base_name='exceptionlog')
error_router.register(r'createexception',views.CreateExceptionViewSet,base_name='createexception')








