#!/bin/sh

SALTUI_PATH=$PWD
PYTHON=$(which python)

$PYTHON $SALTUI_PATH/manage.py migrate

$PYTHON $SALTUI_PATH/manage.py createsuperuser --noinput > /dev/null 2>&1

/usr/local/bin/uwsgi uwsgi.ini
