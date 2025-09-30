# system_views.py
from .system_views.auth_views import SliderVerifyView,LoginView,AuthStatusView,TokenRefreshView,UserProfileView,LogoutView,UserPermissionView
from .system_views.menu_views import MenuListView,MenuCreateView,MenuUpdateView,MenuDeleteView
from .system_views.permission_views import (
    PermissionListView,
    PermissionDetailView,
    PermissionCreateView,
    PermissionUpdateView,
    PermissionDeleteView,
)
