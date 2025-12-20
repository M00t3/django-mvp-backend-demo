#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
# Using gunicorn for production usage in the Docker container
# Bind to 0.0.0.0:8000
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --reload
