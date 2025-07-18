#!/usr/bin/env bash
set -e

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL..."
  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 1
  done
  echo "PostgreSQL is up - continuing"
fi

echo "Applying database migrations"
python manage.py migrate --noinput

echo "Create admin account"
python manage.py createsuperuser --no-input

echo "Collecting static files"
python manage.py collectstatic --noinput

exec "$@"