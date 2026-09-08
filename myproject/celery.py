import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("myproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "remove-expired-records-daily": {
        "task": "accounts.tasks.clean_expired_data",
        "schedule": crontab(hour=1, minute=0),
    },

    "generate-daily-ride-summary": {
        "task": "accounts.tasks.generate_ride_report",
        "schedule": crontab(hour=23, minute=0),
    },

    "clean-old-temporary-data-daily": {
        "task": "accounts.tasks.process_background_records",
        "schedule": crontab(hour=2, minute=0),
    },
}