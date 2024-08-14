#!/bin/sh

python ./manage.py collectstatic --noinput
python ./manage.py migrate
# python ./manage.py compilemessages
gunicorn conf.wsgi:application --workers=3 --bind 0.0.0.0:8000
