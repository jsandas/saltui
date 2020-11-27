from django.urls import re_path

from system_info.views import System_Info

urlpatterns = [
    re_path(r'', System_Info.as_view()),
]
