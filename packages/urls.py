from django.urls import re_path

from packages.views import Hosts, Packages, Summary

urlpatterns = [
    re_path(r'^list_packages/(?P<pkg>.*)$', Packages.as_view()),
    re_path(r'^list_packages[/]?$', Packages.as_view()),
    re_path(r'^list_hosts/(?P<host>\S+)$', Hosts.as_view()),
    re_path(r'^list_hosts[/]?$', Hosts.as_view()),
    re_path(r'', Summary.as_view()),
]
