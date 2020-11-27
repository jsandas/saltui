from django.urls import path, re_path

from users.views import Hosts, Summary, Users
from . import views

urlpatterns = [
    re_path(r'^list_users/(?P<user>\S+)$', Users.as_view()),
    re_path(r'^list_users[/]?$', Users.as_view()),
    re_path(r'^list_hosts/(?P<host>\S+)$', Hosts.as_view()),
    re_path(r'^list_hosts[/]?$', Hosts.as_view()),
    # re_path(r'^list_hosts/(?P<host>\S+)', views.list_hosts, name='hosts'),
    re_path(r'', Summary.as_view()),
]
