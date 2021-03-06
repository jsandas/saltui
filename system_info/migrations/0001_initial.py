# Generated by Django 3.1.2 on 2020-10-06 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host_System_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('system_info', models.JSONField()),
                ('last_update', models.DateTimeField(verbose_name='date updated')),
            ],
            options={
                'db_table': 'host_system_info',
            },
        ),
    ]
