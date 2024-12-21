#!/bin/sh

# Wait for PostgreSQL to be ready
until pg_isready -h "$POSTGRESQL_HOST" -p "$POSTGRESQL_PORT" -U "$POSTGRESQL_USERNAME"; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

python manage.py migrate
celery -A user_service worker --loglevel=info &
python manage.py runserver 0.0.0.0:8001
