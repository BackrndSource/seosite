#!/bin/sh

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

gunicorn seosite.wsgi:application --bind 0.0.0.0:8000 -w 4