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
def check_unstarted_event():
    now = timezone.now()
    now = now - datetime.timedelta(minutes=10)
    events = Event.objects.filter(date_event__lte=now, status=1)
    for event in events:
        try:
            event.episode.exists()
        except Exception:
            event.status = 3
            event.save()
            send_entry_notification_email.delay(
                event.creator_id,
                event.event_name + " Status",
                event.event_name + " cancelled."
            )
            if event.contestant1 is not None:
                send_entry_notification_email.delay(
                    event.contestant1_id,
                    event.event_name + " Status",
                    event.event_name + " cancelled."
                )
            if event.contestant2 is not None:
                send_entry_notification_email.delay(
                    event.contestant2_id,
                    event.event_name + " Status",
                    event.event_name + " cancelled."
                )


@app.task
def send_entry_notification_email(user_id, subject, body):
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            subject,
            body,
            'channelshowdown2018@gmail.com',
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
            'channelshowdown2018@gmail.com',
            email_list,
            fail_silently=False,
        )


@app.task
def close_voting():
    now = timezone.now()
    now = now - datetime.timedelta(minutes=30)
    events = Event.objects.filter(status=2, date_ended__lte=now)
    for event in events:
        event.voting_status = 1
        event.save()
