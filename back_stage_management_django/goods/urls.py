from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecificationCategoryViewSet, ProductViewSet
app_name='goods'
router = DefaultRouter()
router.register('spec-categories', SpecificationCategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

# from django.urls import path
# from . import views
#
# # 指定应用命名空间
# app_name='goods'
#
# urlpatterns = [
#     path('good/',views.book_list)
# ]
