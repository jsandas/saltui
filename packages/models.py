from django.contrib.postgres.fields import JSONField
from django.db import models

class Host_Packages(models.Model):
    name = models.CharField(max_length=200)
    total = models.IntegerField()
    packages = models.JSONField()
    updates = models.IntegerField()
    last_update = models.DateTimeField('date updated')

    class Meta:
        db_table = "host_packages"

    def __str__(self):
        return self.name

class Package_Hosts(models.Model):
    name = models.CharField(max_length=200)
    total = models.IntegerField()
    hosts = models.JSONField()
    updates = models.IntegerField()
    last_update = models.DateTimeField('date updated')

    class Meta:
        db_table = "package_hosts"

    def __str__(self):
        return self.name