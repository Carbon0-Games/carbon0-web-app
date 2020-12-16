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
# python manage.py runserver 0.0.0.0:8000
gunicorn carbon0.wsgi:application --bind 0.0.0.0:8000