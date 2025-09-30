from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # 用户授权
    path('slider_verify/', SliderVerifyView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('status/', AuthStatusView.as_view(), name='auth-status'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userinfo/', UserProfileView.as_view(), name='user-profile'),
    path('permission/', UserPermissionView.as_view(), name='user-permission'),
    #菜单管理
    path('menus/', MenuListView.as_view()),
    path('menus/create/', MenuCreateView.as_view()),
    path('menus/update/<int:menu_id>/', MenuUpdateView.as_view()),
    path('menus/delete/<int:menu_id>/', MenuDeleteView.as_view()),
    #权限管理
    path('permissions/', PermissionListView.as_view()),
    path('permissions/<int:pk>/', PermissionDetailView.as_view()),
    path('permissions/create/', PermissionCreateView.as_view()),
    path('permissions/update/<int:pk>/', PermissionUpdateView.as_view()),
    path('permissions/delete/<int:pk>/', PermissionDeleteView.as_view()),
]

