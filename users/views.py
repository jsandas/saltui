from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from users.models import Host_Users, User_Hosts


class Summary(LoginRequiredMixin, TemplateView):
    template_name = 'users/summary.html'
    title = 'Summary'

    def data(self):
        hosts = Host_Users.objects.order_by('name')
        users = User_Hosts.objects.order_by('name')

        context = {
            'hosts': hosts,
            'users': users
        }

        return context


class Users(LoginRequiredMixin, TemplateView):
    template_name = 'users/users.html'
    title = 'Users'

    def data(self):
        single_user = None

        if 'user' in self.kwargs.keys():
            single_user = self.kwargs['user']

        if single_user:
            users = User_Hosts.objects.filter(name__exact=single_user)
        else:
            users = User_Hosts.objects.order_by('name')

        context = {
            'users': users
        }

        return context


class Hosts(LoginRequiredMixin, TemplateView):
    template_name = 'users/hosts.html'
    title = 'Host'

    def data(self):
        single_host = None

        if 'host' in self.kwargs.keys():
            single_host = self.kwargs['host']

        if single_host:
            hosts = Host_Users.objects.filter(name__exact=single_host)
        else:
            hosts = Host_Users.objects.order_by('name')

        context = {
            'hosts': hosts
        }

        return context
