from django.views.generic import TemplateView
from system_info.models import Host_System_Info

class System_Info(TemplateView):
    template_name = 'system_info/summary.html'
    title = 'Summary'

    def data(self):
        hosts = Host_System_Info.objects.order_by('name')

        context = {
            'hosts': hosts,
        }

        return context
