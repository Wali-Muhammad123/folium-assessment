#!/bin/bash

# Activate the virtual environment
source /venv/bin/activate

# Start the Celery worker
/venv/bin/celery -A warehouse.celery_app worker &

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
