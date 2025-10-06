from django.urls import path
from user_permission.system_views.department_views import *

department_urlpatterns = [
    path("", DepartmentListView.as_view(), name='department-list'),
    path("create/", DepartmentCreateView.as_view(), name='department-create'),
    path("update/<int:dept_id>/", DepartmentUpdateView.as_view(), name='department-update'),
    path("delete/<int:dept_id>/", DepartmentDeleteView.as_view(), name='department-delete'),
    path("principal/", ActiveUserListAPIView.as_view(), name='department-principal'),
]