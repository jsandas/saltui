from django.contrib.postgres.fields import JSONField
from django.db import models

class Host_Users(models.Model):
    name = models.CharField(max_length=200)
    total = models.IntegerField()
    users = models.JSONField()
    last_update = models.DateTimeField('date updated')

    class Meta:
        db_table = "host_users"

    def __str__(self):
        return self.name

class User_Hosts(models.Model):
    name = models.CharField(max_length=200)
    total = models.IntegerField()
    hosts = models.JSONField()
    last_update = models.DateTimeField('date updated')

    class Meta:
        db_table = "user_hosts"

    def __str__(self):
        return self.name