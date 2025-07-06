#!/bin/bash

MANAGEPY="python /app/app/manage.py"

echo "Applying migrations..."
${MANAGEPY} makemigrations
${MANAGEPY} migrate --noinput

DJANGO_SUPERUSER_PASSWORD=admin ${MANAGEPY} createsuperuser \
    --no-input \
    --username=admin \
    --email=cfattarsi@gmail.com

${MANAGEPY} collectstatic --noinput

cd /app/app/
gunicorn app.wsgi:application --bind 0.0.0.0:8844
