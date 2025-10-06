from django.urls import path
from user_permission.system_views.menu_views import *

menu_urlpatterns = [
    path('', MenuListView.as_view(), name='menu-list'),
    path('create/', MenuCreateView.as_view(), name='menu-create'),
    path('update/<int:menu_id>/', MenuUpdateView.as_view(), name='menu-update'),
    path('delete/<int:menu_id>/', MenuDeleteView.as_view(), name='menu-delete'),
]