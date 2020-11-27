import time
from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from packages.models import Host_Packages, Package_Hosts

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
            Host_Packages.objects.all().delete()
            Package_Hosts.objects.all().delete()
            return

        timestamp = timezone.now()

        if settings.PURGE_OLD_RECORDS:
            ts = timestamp - timedelta(settings.PURGE_OLDER_THAN)
            Host_Packages.objects.filter(last_update__lt=ts).delete()
            Package_Hosts.objects.filter(last_update__lt=ts).delete()

        client = salt_client()

        installed_packages = client.cmd(kwargs['target'], 'pkg.list_pkgs', tgt_type='compound', batch=5)
        # package_upgrades = client.cmd(kwargs['target'], 'pkg.list_upgrades', kwarg={'enablerepo':'digicert,saltstack,mariadb,datastax-dse'},tgt_type='compound', batch=5)
        package_upgrades = client.cmd(kwargs['target'], 'pkg.list_upgrades', tgt_type='compound', batch=5)

        packages_list = {}
        packages_list['hosts'] = {}

        try:
            for host, packages in installed_packages.items():
                packages_list = {}
                if not packages:
                    self.stdout.write(self.style.WARN('No packages information for {}'.format(host)))
                    packages_list['packages'] = {}
                    packages_list['total'] = 0
                    packages_list['updates'] = 0

                if packages:
                    packages_list['packages'] = {}
                    packages_list['total'] = 0
                    packages_list['updates'] = 0
                    for package, version in packages.items():
                        packages_list['total'] += 1
                        packages_list['packages'][package] = {}
                        if package in package_upgrades[host]:
                            new_version = package_upgrades[host][package]
                            packages_list['packages'][package]['current'] = version
                            packages_list['packages'][package]['latest'] = new_version
                            packages_list['updates'] += 1
                        else:
                            packages_list['packages'][package]['current'] = version
                            packages_list['packages'][package]['latest'] = 'N/A'


                obj, created = Host_Packages.objects.update_or_create(name=host, 
                        defaults={'total': packages_list['total'], 
                                'packages': packages_list['packages'], 
                                'updates': packages_list['updates'], 
                                'last_update': timestamp})
                obj.save()

            self.stdout.write(self.style.SUCCESS('Updated host packages table'))
        except Exception as e:
            self.stdout.write(self.style.WARNING('Failed getting package information: ', e))
            self.stdout.write(self.style.WARNING('package data: {}'.format(installed_packages)))
            self.stdout.write(self.style.WARNING('update data: {}'.format(package_upgrades)))

        temp_package_list = {}
        try:
            for host, packages in installed_packages.items():
                if packages == False:
                    continue

                for package, version in packages.items():
                    temp_package_list[package] = {}
                    temp_package_list[package]['hosts'] = {} 
                    temp_package_list[package]['total'] = 0
                    temp_package_list[package]['updates'] = 0
                
            for pkg in temp_package_list:
                for host, packages in installed_packages.items():
                    if packages == False:
                        continue
                    for package, version in packages.items():
                        if pkg == package:
                            temp_package_list[package]['hosts'][host] = {}
                            temp_package_list[package]['total'] += 1
                            if package in package_upgrades[host]:
                                new_version = package_upgrades[host][package]
                                temp_package_list[package]['hosts'][host]['current'] = version
                                temp_package_list[package]['hosts'][host]['latest'] = new_version
                                temp_package_list[package]['updates'] += 1
                            else:
                                temp_package_list[package]['hosts'][host]['current'] = version
                                temp_package_list[package]['hosts'][host]['latest'] = 'N/A'


            for package, data in temp_package_list.items():
                obj, created = Package_Hosts.objects.update_or_create(name=package, 
                        defaults={'total': data['total'], 
                                'hosts': data['hosts'], 
                                'updates': data['updates'], 
                                'last_update': timestamp})
                obj.save()                   

            self.stdout.write(self.style.SUCCESS('Updated package hosts table'))
        except Exception as e:
            self.stdout.write(self.style.WARNING('Failed getting package information: ', e))
            self.stdout.write(self.style.WARNING('package data: {}'.format(installed_packages)))
            self.stdout.write(self.style.WARNING('update data: {}'.format(package_upgrades)))