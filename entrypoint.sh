#!/bin/bash

# Wait for MySQL to be ready
until (echo > /dev/tcp/$MYSQL_HOST/$MYSQL_PORT) >/dev/null 2>&1; do
  echo "Waiting for MySQL server to start..."
  sleep 5
done

echo "MySQL is up and running. Starting Django application."

# Run the Django application
python manage.py runserver 0.0.0.0:8000
