#!/bin/sh

until python check.py; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

