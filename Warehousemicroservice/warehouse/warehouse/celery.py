# celery.py (in your_project_name app)
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")
app = Celery("warehouse")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
