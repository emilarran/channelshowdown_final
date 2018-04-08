from channelshowdown.celery import app
from .models import Event
from datetime import datetime


@app.task
def check_event_date():
    now = datetime.now()
    events = Event.objects.filter(date_event__gte=now)
    for event in events:
        event.status = 1
        event.save()


# @app.task
# def sample_task():
#     print("this is a sample")
