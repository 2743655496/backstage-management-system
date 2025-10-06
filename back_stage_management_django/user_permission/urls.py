from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 导入各个模块的路由
from user_permission.my_urls.auth_urls import auth_urlpatterns
from user_permission.my_urls.menu_urls import menu_urlpatterns
from user_permission.my_urls.permission_urls import permission_urlpatterns
from user_permission.my_urls.department_urls import department_urlpatterns
from user_permission.my_urls.role_urls import role_urlpatterns
from user_permission.my_urls.user_urls import user_urlpatterns

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # 认证授权模块
    path('auth/', include(auth_urlpatterns)),
    # 系统管理模块
    path('menus/', include(menu_urlpatterns)),
    path('permissions/', include(permission_urlpatterns)),
    path('departments/', include(department_urlpatterns)),
    path('roles/', include(role_urlpatterns)),
    path('users/', include(user_urlpatterns)),
]
