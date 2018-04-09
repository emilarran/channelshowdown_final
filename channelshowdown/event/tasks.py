from channelshowdown.celery import app
from django.utils import timezone
from .models import Event


@app.task
def check_event_date():
    now = timezone.now()
    events = Event.objects.filter(date_event__lte=now, status=0)
    for event in events:
        print(event)
        event.status = 1
        event.save()
