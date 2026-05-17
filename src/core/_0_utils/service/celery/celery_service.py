import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_0_config.settings")

app = Celery("_0_config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
