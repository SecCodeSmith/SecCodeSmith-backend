#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the database to be ready
# This is a good practice to avoid race conditions on startup.
if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL..."
  # Use netcat to check if the database host and port are available
  while ! nc -z "$DATABASE_HOST" 5432; do
    sleep 1
  done
  echo "PostgreSQL is up - continuing"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Checking for superuser..."
python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    print("Superuser not found, creating one...")
    if username and email and password:
        User.objects.create_superuser(username, email, password)
        print("Superuser created.")
    else:
        print("Superuser environment variables are not set. Skipping creation.")
else:
    print("Superuser already exists.")
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting server..."
exec "$@"
