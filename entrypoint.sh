#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z mentor-portal-db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

python main.py recreate_db

python main.py seed_db

python main.py run -h 0.0.0.0
