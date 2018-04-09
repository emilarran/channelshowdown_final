from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channelshowdown.settings')

app = Celery('channelshowdown')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-event-date-every-minute': {
        'task': 'event.tasks.check_event_date',
        'schedule': crontab(),
    }
}