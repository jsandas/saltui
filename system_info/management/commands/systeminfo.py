import time
from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from system_info.models import Host_System_Info

if settings.SALT_CLIENT == 'local':
    from utils.salt_client import local_client as salt_client
else:
    from utils.salt_client import api_client as salt_client

class Command(BaseCommand):
    help = 'manage data for system_info application'

    def add_arguments(self, parser):
        parser.add_argument('--truncate', action='store_true', help='truncate data')

        parser.add_argument('--update', action='store_true', help='update data')

        parser.add_argument('--target', action='store', dest='target',
                            help='Set minion target data', default='*')

    def handle(self, *args, **kwargs):
        """
        Command to create list of system information/stats
        """

        if kwargs['truncate']:
            Host_System_Info.objects.all().delete()
            return

        timestamp = timezone.now()

        if settings.PURGE_OLD_RECORDS:
            ts = timestamp - timedelta(settings.PURGE_OLDER_THAN)
            obj = Host_System_Info.objects.filter(last_update__lt=ts).delete()

        client = salt_client()
        system_grains = client.cmd(kwargs['target'], 'grains.item',
                    ['cpuarch','env','ipv4','mem_total','num_cpus',
                    'os','osmajorrelease','osrelease','osversion',
                    'role','selinux','server_category','swap_total'], tgt_type='compound', batch=5)

        try:
            for host, grains in system_grains.items():
                # grains will be false if the mininon did not respond
                if grains:
                    grains['disk_total'] = 0
                    grains['disk_used'] = 0
                    grains['disk_free'] = 0

                    disk_info = client.cmd(host, 'disk.usage', tgt_type='compound')
                    for _, data in disk_info[host].items():
                        if data['1K-blocks']:
                            grains['disk_total'] += int(int(data['1K-blocks']) / 1024)
                        if data['used']:  
                            grains['disk_used'] += int(int(data['used']) / 1024)
                        if data['available']:
                            grains['disk_free'] += int(int(data['available']) / 1024)

                else:
                    grains = {}

                obj, created = Host_System_Info.objects.update_or_create(name=host, 
                        defaults={'system_info': grains, 'last_update': timestamp})
                obj.save()

            self.stdout.write(self.style.SUCCESS('Updated system_info table'))
        except Exception as e:
            self.stdout.write(self.style.WARNING('Failed getting system information: ', e))
            self.stdout.write(self.style.WARNING('Grain data: {}'.format(system_grains))) 
