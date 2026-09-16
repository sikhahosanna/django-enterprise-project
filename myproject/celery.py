import os

from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab


# Load environment variables
load_dotenv()


# Get current environment
environment = os.getenv(
    "DJANGO_ENV",
    "development"
).lower()


# Select Django settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"myproject.settings.{environment}"
)


# Create Celery application
app = Celery("myproject")


# Load Celery configuration from Django settings
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)


# Automatically discover tasks
app.autodiscover_tasks()


# Celery Beat Schedule
app.conf.beat_schedule = {

    "remove-expired-records-daily": {
        "task": "accounts.tasks.clean_expired_data",
        "schedule": crontab(
            hour=1,
            minute=0
        ),
    },

    "generate-daily-ride-summary": {
        "task": "accounts.tasks.generate_ride_report",
        "schedule": crontab(
            hour=23,
            minute=0
        ),
    },

    "clean-old-temporary-data-daily": {
        "task": "accounts.tasks.process_background_records",
        "schedule": crontab(
            hour=2,
            minute=0
        ),
    },

}