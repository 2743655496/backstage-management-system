from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, RoleViewSet, UserViewSet, PermissionViewSet
from .views import LoginView, TokenRefreshView, UserProfileView,LogoutView,SliderVerifyView,AuthStatusView,UserPermissionView

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('slider_verify/', SliderVerifyView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('status/', AuthStatusView.as_view(), name='auth-status'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userinfo/', UserProfileView.as_view(), name='user-profile'),
    path('permission/', UserPermissionView.as_view(), name='user-permission'),
]

