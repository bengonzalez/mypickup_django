#!/bin/sh
set -e

python manage.py migrate --noinput

exec gunicorn mypickup_django.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
