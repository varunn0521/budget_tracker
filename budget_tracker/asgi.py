from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('budget_tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat schedule
from celery.schedules import crontab
app.conf.beat_schedule = {
    'deduct-emis-daily': {
        'task': 'tracker.tasks.process_emis',  # replace 'tracker' with your app name
        'schedule': crontab(minute=0, hour=0),  # This will run every day at midnight
    },
}
