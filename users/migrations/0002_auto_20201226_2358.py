# Generated by Django 3.1.4 on 2020-12-26 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host_users',
            name='users',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='user_hosts',
            name='hosts',
            field=models.JSONField(default=dict),
        ),
    ]
