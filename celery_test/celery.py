from celery import Celery
app = Celery("celery_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

