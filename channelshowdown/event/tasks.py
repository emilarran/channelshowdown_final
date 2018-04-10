from channelshowdown.celery import app
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .models import Event
from django.contrib.auth.models import User
from django.core.mail import send_mail
import logging
# from django.


@app.task
def check_event_date():
    now = timezone.now()
    events = Event.objects.filter(date_event__lte=now, status=0)
    for event in events:
        print(event)
        event.status = 1
        event.save()


@app.task
def send_entry_notification_email(user_id, subject, body):
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            subject,
            body,
            'channelfix.channelshowdown@gmail.com',
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning("Tried to send email to non-existing user.")
