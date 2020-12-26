from django.contrib.postgres.fields import JSONField
from django.db import models

class Host_System_Info(models.Model):
    name = models.CharField(max_length=200)
    system_info = models.JSONField(default=dict)
    highstate_status = models.BooleanField(default=False)
    missing_hs_states = models.JSONField(default=dict)
    last_update = models.DateTimeField('date updated')

    class Meta:
        db_table = "host_system_info"

    def __str__(self):
        return self.name