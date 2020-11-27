#!/bin/sh

python manage.py migrate

/usr/local/bin/uwsgi uwsgi.ini
