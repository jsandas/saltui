from django.views.generic import TemplateView
from packages.models import Host_Packages, Package_Hosts


class Summary(TemplateView):
    template_name = 'packages/summary.html'
    title = 'Summary'

    def data(self):
        hosts = Host_Packages.objects.order_by('name')
        packages = Package_Hosts.objects.order_by('name')

        context = {
            'hosts': hosts,
            'packages': packages
        }

        return context


class Packages(TemplateView):
    template_name = 'packages/packages.html'
    title = 'Packages'

    def data(self):
        single_package = None

        if 'pkg' in self.kwargs.keys():
            single_package = self.kwargs['pkg']

        if single_package:
            packages = Package_Hosts.objects.filter(name__exact=single_package)
        else:
            packages = Package_Hosts.objects.order_by('name')

        context = {
            'packages': packages
        }

        return context


class Hosts(TemplateView):
    template_name = 'packages/hosts.html'
    title = 'Hosts'

    def data(self):
        single_host = None

        if 'host' in self.kwargs.keys():
            single_host = self.kwargs['host']

        if single_host:
            hosts = Host_Packages.objects.filter(name__exact=single_host)
        else:
            hosts = Host_Packages.objects.order_by('name')

        context = {
            'hosts': hosts
        }

        return context
