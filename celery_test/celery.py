# django_celery/celery.py

import os
from celery import Celery

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_test.settings__cache")
app = Celery("celery_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

