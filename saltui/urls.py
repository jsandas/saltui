from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('packages/', include('packages.urls')),
    path('users/', include('users.urls')),
    path('system_info/', include('system_info.urls'))
]
