import os
import django
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Django
try:
    django.setup()
except RuntimeError:
    # Django is already set up, ignore
    pass

celery_app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Configure broker connection to be lazy (don't connect until needed)
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_connection_retry = True
celery_app.conf.broker_connection_max_retries = 10

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()