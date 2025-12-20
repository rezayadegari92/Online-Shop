import os

import django
from celery import Celery
from celery.schedules import crontab

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

# Explicitly import cache warming tasks to register them
try:
    import core.cache_warming  # noqa: F401
except ImportError:
    pass

# Celery Beat Schedule for Cache Warming
# Prevents cache stampede by proactively refreshing cache before expiration
celery_app.conf.beat_schedule = {
    # Warm all critical caches every 5 minutes
    "warm-all-critical-caches": {
        "task": "cache.warm_all_critical",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
        "options": {"expires": 240},  # Task expires after 4 minutes
    },
    # Warm product list more frequently (every 3 minutes)
    "warm-product-list": {
        "task": "cache.warm_product_list",
        "schedule": crontab(minute="*/3"),  # Every 3 minutes
        "options": {"expires": 120},
    },
    # Warm top products every 5 minutes
    "warm-top-products": {
        "task": "cache.warm_top_products",
        "schedule": crontab(minute="*/5"),
        "options": {"expires": 240},
    },
    # Warm categories less frequently (every 15 minutes)
    "warm-categories": {
        "task": "cache.warm_categories",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
        "options": {"expires": 600},
    },
    # Warm brands less frequently (every 15 minutes)
    "warm-brands": {
        "task": "cache.warm_brands",
        "schedule": crontab(minute="*/15"),
        "options": {"expires": 600},
    },
}

# Set default timezone for beat scheduler
celery_app.conf.timezone = "UTC"
