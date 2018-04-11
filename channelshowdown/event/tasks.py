from channelshowdown.celery import app
from django.utils import timezone
from .models import Event
from django.contrib.auth.models import User
from django.core.mail import send_mail
import datetime
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


@app.task
def send_notification_event_start():
    now = timezone.now()
    now = now + datetime.timedelta(hours=1)
    events = Event.objects.filter(date_event__lte=now, status=0)
    for event in events:
        creator = User.objects.get(pk=event.creator_id)
        email_list = [creator.email]
        try:
            contestant1 = User.objects.get(pk=event.contestant1_id)
            email_list.append(contestant1.email)
        except User.DoesNotExist:
            pass
        try:
            contestant2 = User.objects.get(pk=event.contestant2_id)
            email_list.append(contestant2.email)
        except User.DoesNotExist:
            pass
        send_mail(
            event.event_name + " is About to Start",
            "Your event is about to start, please get ready.",
            'channelfix.channelshowdown@gmail.com',
            email_list,
            fail_silently=False,
        )
