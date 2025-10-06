"""
URL configuration for back_stage_management_django project.

The `urlpatterns` list routes URLs to system_views2. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function system_views2
    1. Add an import:  from my_app import system_views2
    2. Add a URL to urlpatterns:  path('', system_views2.home, name='home')
Class-based system_views2
    1. Add an import:  from other_app.system_views2 import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('goods/',include("goods.urls")),
    path('api/system/',include("user_permission.urls"))
]
