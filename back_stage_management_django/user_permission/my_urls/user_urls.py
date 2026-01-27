from django.urls import path
from user_permission.system_views.user_views import *

user_urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('detail_update/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail-update'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),

]
