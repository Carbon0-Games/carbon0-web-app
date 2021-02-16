#!/bin/sh

# Credit to Mausam Gaurav, who posted the Dockerfile I used as a starting point
# on this blog: 
# https://datagraphi.com/blog/post/2020/8/30/docker-guide-build-a-fully-production-ready-machine-learning-app-with-react-django-and-postgresql-on-docker

# make sure PostgreSQL is running before we migrate data and SQL schema
 if [ "$DATABASE" = "postgres" ]
 then
     echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# use local settings
export DJANGO_SETTINGS_MODULE=carbon0.settings.local
# migrate data and SQL schema
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py loaddata carbon_quiz/fixtures/mission_link_data.json carbon_quiz/fixtures/question_data.json

# Make a superuser account if not already available, and add a Profile for it
echo "
from django.contrib.auth import get_user_model
from accounts.models.profile import Profile
admin_objs = get_user_model().objects.filter(email='$DJANGO_ADMIN_EMAIL')
if len(admin_objs) == 0:
  admin_obj = get_user_model().objects.create_superuser(
    '$DJANGO_ADMIN_USER', 
    '$DJANGO_ADMIN_EMAIL', 
    '$DJANGO_ADMIN_PASSWORD',
  )
  Profile.objects.get_or_create(user=admin_obj)" | python manage.py shell

# The test command has been commented out - turn it back on whenever you specifically want
# to run the tests within Docker!
# python manage.py test

# run the Django project
gunicorn carbon0.wsgi:application --bind 0.0.0.0:8000