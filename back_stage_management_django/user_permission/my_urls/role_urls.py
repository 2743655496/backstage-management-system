from django.urls import path
from user_permission.system_views.role_views import *

role_urlpatterns = [
    path('', RoleListCreateView.as_view(), name='role-list-create'),
    path('detail_update/<int:pk>/', RoleDetailView.as_view(), name='role-detail-update'),
    path('delete/<int:pk>/', RoleDeleteView.as_view(), name='role-delete'),
]