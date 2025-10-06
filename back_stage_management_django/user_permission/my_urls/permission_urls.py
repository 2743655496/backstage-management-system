from django.urls import path
from user_permission.system_views.permission_views import *

permission_urlpatterns = [
    path('', PermissionListView.as_view(), name='permission-list'),
    path('create/', PermissionCreateView.as_view(), name='permission-create'),
    path('update/<int:pk>/', PermissionUpdateView.as_view(), name='permission-update'),
    path('delete/<int:pk>/', PermissionDeleteView.as_view(), name='permission-delete'),
]