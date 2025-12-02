import os
import django
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Django before creating Celery app (only if not already initialized)
if not django.apps.apps.ready:
    django.setup()

celery_app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()