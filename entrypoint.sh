#!/bin/sh
python manage.py collectstatic --noinput
python manage.py migrate --noinput
