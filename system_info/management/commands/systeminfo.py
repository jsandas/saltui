import json

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

        self._get_info(kwargs['target'], timestamp)


    def _get_info(self, target, timestamp):
        client = salt_client()
        system_grains = client.cmd(target, 'grains.item',
                    ['cpuarch','env','ipv4','kernel','kernelrelease','mem_total','num_cpus',
                    'os','osmajorrelease','osrelease','osversion',
                    'role','selinux','server_category','swap_total'], tgt_type='compound', batch=5)

        for host, grains in system_grains.items():
            # grains will be false if the minion did not respond
            if grains:
                grains['disk_total'] = 0
                grains['disk_used'] = 0
                grains['disk_free'] = 0

                disk_info = client.cmd(host, 'disk.usage', tgt_type='compound')
                try:
                    for _, data in disk_info[host].items():
                        if data['1K-blocks']:
                            grains['disk_total'] += int(int(data['1K-blocks']) / 1024)
                        if data['used']:
                            grains['disk_used'] += int(int(data['used']) / 1024)
                        if data['available']:
                            grains['disk_free'] += int(int(data['available']) / 1024)
                except:
                    self.stdout.write(self.style.ERROR('host {} bad disk.usage return: {}'.format(target, disk_info[host])))
                
                hs_info = self._get_highstate(host)

            else:
                grains = {}
                hs_info = {'status': False,
                            'missing_states': {}
                }

            results = {'system_info': grains,
                        'highstate_status': hs_info['status'],
                        'missing_hs_states': hs_info['missing_states'],
                        'last_update': timestamp
                    }

            obj, created = Host_System_Info.objects.update_or_create(name=host, defaults = (results))
            if created:
                self.stdout.write(self.style.SUCCESS('Added new host "{}" to system_info table'.format(host)))

            obj.save()

        self.stdout.write(self.style.SUCCESS('Finished updating system_info table'))


    def _get_highstate(self, target):
        ret = {'status': False,
                'missing_states': {}
            }

        client = salt_client()

        highstate_return = client.cmd(target, 'state.apply',
                    kwarg={'test': True}, tgt_type='compound')

        states = highstate_return[target]

        if states:
            missing_states = {}
            try:
                for name, state in states.items():
                    if not state['result']:
                        self.stdout.write(self.style.WARNING('host {} not compliant with {}'.format(target, name)))
                        missing_states[name] = state['comment']
                
                if missing_states:
                    ret['missing_states'] = missing_states
                else:
                    ret['status'] = True
            except:
                self.stdout.write(self.style.ERROR('host {} bad highstate return: {}'.format(target, states)))
        return ret