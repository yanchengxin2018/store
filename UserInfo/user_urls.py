from rest_framework.routers import DefaultRouter
from UserInfo import views as userinfo_views


user_router=DefaultRouter()
user_router.register('Login',userinfo_views.LoginViewSet,base_name='user_Login')
user_router.register('LoginOut',userinfo_views.LoginOutViewSet,base_name='user_LoginOut')
user_router.register('Register',userinfo_views.RegisterViewSet,base_name='user_Register')
user_router.register('IsLogin',userinfo_views.IsLoginViewSet,base_name='user_IsLogin')
user_router.register('UpdataAPI',userinfo_views.UpdataAPIViewSet,base_name='user_UpdataAPI')
user_router.register('API',userinfo_views.APIViewSet,base_name='user_API')
user_router.register('Users',userinfo_views.UsersViewSet,base_name='user_Users')
user_router.register('Roles',userinfo_views.RolesViewSet,base_name='user_Roles')
user_router.register('changeuser',userinfo_views.ChangeUserViewSet,base_name='user_changeuser')




