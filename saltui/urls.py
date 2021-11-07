from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('packages/', include('packages.urls')),
    path('system_info/', include('system_info.urls')),
    path('users/', include('users.urls')),
]
