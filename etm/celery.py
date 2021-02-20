import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etm.settings')

app = Celery('etm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'api.tasks.create_report',
        'schedule': crontab(day_of_week = 'sunday'),
        'args': (),
    },
}
app.autodiscover_tasks()