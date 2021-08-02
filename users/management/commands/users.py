import time
from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from users.models import User_Hosts, Host_Users

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
            User_Hosts.objects.all().delete()
            Host_Users.objects.all().delete()
            return

        timestamp = timezone.now()

        if settings.PURGE_OLD_RECORDS:
            ts = timestamp - timedelta(settings.PURGE_OLDER_THAN)
            User_Hosts.objects.filter(last_update__lt=ts).delete()
            Host_Users.objects.filter(last_update__lt=ts).delete()

        client = salt_client()

        user_data = client.cmd(kwargs['target'], 'user.getent',tgt_type='compound', batch=5)
        # lastlog_data = client.cmd(kwargs['target'], 'userinfo.lastlog',tgt_type='compound', batch=5)

        missing_lastlog = False
        hosts_users = {}
        hosts_users['hosts'] = {}
        users_hosts = {}
        users_hosts['users'] = {}

        for host, users in user_data.items():
            hosts_users['hosts'][host] = {}
            hosts_users['hosts'][host]['users'] = {}
            count = 0
        
            # lastlog_errors = ['Unsupported OS', 'Unable to find or open the file: /var/log/lastlog', "'userinfo.lastlog' is not available."]
            # if lastlog_data[host] in lastlog_errors:
            #     missing_lastlog = True
            #     fix_command = ' salt {} saltutil.sync_modules'.format(host)
            #     self.stdout.write(self.style.WARNING('Lastlog information not available on minion {} error: {}'.format(host, lastlog_data[host])))
            if users:
                for user in users:
                    count += 1
                    name = user['name']

                    users_hosts['users'][name] = {}

                    hosts_users['hosts'][host]['users'][name] = {}

                    # Windows minions do not have fullname in returned data
                    if 'fullname' in user:
                        hosts_users['hosts'][host]['users'][name]['fullname'] = user['fullname']
                    else:
                        hosts_users['hosts'][host]['users'][name]['fullname'] = user['name']
                    hosts_users['hosts'][host]['users'][name]['home'] = user['home']
                    hosts_users['hosts'][host]['users'][name]['uid'] = user['uid']
                    hosts_users['hosts'][host]['users'][name]['gid'] = user['gid']
                    hosts_users['hosts'][host]['users'][name]['groups'] = user['groups']
                    hosts_users['hosts'][host]['users'][name]['shell'] = user['shell']
                    hosts_users['hosts'][host]['total'] = count

                    hosts_users['hosts'][host]['users'][name]['last_login'] = 'not available'
                    hosts_users['hosts'][host]['users'][name]['client_ip'] = 'not available'
                    # if missing_lastlog:
                    #     hosts_users['hosts'][host]['users'][name]['last_login'] = 'not available'
                    #     hosts_users['hosts'][host]['users'][name]['client_ip'] = 'not available'
                    # elif lastlog_data[host]['users'][name]:
                    #     hosts_users['hosts'][host]['users'][name]['last_login'] = lastlog_data[host]['users'][name]['last_login']
                    #     hosts_users['hosts'][host]['users'][name]['client_ip'] = lastlog_data[host]['users'][name]['client_ip']
                    # else:
                    #     message = 'User {} not found in lastlog on {}'.format(name, host)
                    #     hosts_users['hosts'][host]['users'][name]['last_login'] = 'User not in lastlog'
                    #     hosts_users['hosts'][host]['users'][name]['client_ip'] = 'User not in lastlog'
            else:
                self.stdout.write(self.style.WARNING('No user information for {}'.format(host)))
                hosts_users['hosts'][host]['users'] = {}
                hosts_users['hosts'][host]['total'] = 0

            obj, created = Host_Users.objects.update_or_create(name=host, 
                    defaults={'total': hosts_users['hosts'][host]['total'], 
                            'users': hosts_users['hosts'][host]['users'], 
                            'last_update': timestamp})
            if created:
                self.stdout.write(self.style.SUCCESS('Added new host {} to host_users table'.format(host)))

            obj.save()

        self.stdout.write(self.style.SUCCESS('Finished updating host_users table'))

        for user in users_hosts['users']:
            users_hosts['users'][user]['hosts'] = {}
            count = 0
            for host, host_data in hosts_users['hosts'].items():
                if user in host_data['users']:
                    count += 1
                    users_hosts['users'][user]['hosts'][host] = {}
                    users_hosts['users'][user]['hosts'][host]['fullname'] = hosts_users['hosts'][host]['users'][user]['fullname']
                    users_hosts['users'][user]['hosts'][host]['home'] = hosts_users['hosts'][host]['users'][user]['home']
                    users_hosts['users'][user]['hosts'][host]['uid'] = hosts_users['hosts'][host]['users'][user]['uid']
                    users_hosts['users'][user]['hosts'][host]['gid'] = hosts_users['hosts'][host]['users'][user]['gid']
                    users_hosts['users'][user]['hosts'][host]['groups'] = hosts_users['hosts'][host]['users'][user]['groups']
                    users_hosts['users'][user]['hosts'][host]['shell'] = hosts_users['hosts'][host]['users'][user]['shell']
                    users_hosts['users'][user]['hosts'][host]['last_login'] = hosts_users['hosts'][host]['users'][user]['last_login']
                    users_hosts['users'][user]['hosts'][host]['client_ip'] = hosts_users['hosts'][host]['users'][user]['client_ip']
            users_hosts['users'][user]['total'] = count

            obj, created = User_Hosts.objects.update_or_create(name=user, 
                defaults={'total':users_hosts['users'][user]['total'], 
                        'hosts': users_hosts['users'][user]['hosts'], 
                        'last_update': timestamp})

            if created:
                self.stdout.write(self.style.SUCCESS('Added new user {} to user_hosts table'.format(user)))

            obj.save()

        self.stdout.write(self.style.SUCCESS('Finished updating user_hosts table'))
