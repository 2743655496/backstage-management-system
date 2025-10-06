from django.urls import path
from user_permission.system_views.auth_views import *

auth_urlpatterns = [
    path('slider_verify/', SliderVerifyView.as_view(), name='slider-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('status/', AuthStatusView.as_view(), name='auth-status'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userinfo/', UserProfileView.as_view(), name='user-profile'),
    path('permission/', UserPermissionView.as_view(), name='user-permission'),
]