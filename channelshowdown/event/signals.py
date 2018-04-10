from .models import Event, Entry
from userprofile.models import Notification
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from event.tasks import send_entry_notification_email
import os


@receiver(pre_save, sender=Event)
def delete_unused_eventinfo_file(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_pic = Event.objects.get(pk=instance.pk).event_image
    except Event.DoesNotExist:
        return False

    new_pic = instance.event_image
    if (not old_pic == new_pic) & (not old_pic.url == '/media/profile_image/default.jpg'):
        if os.path.isfile(old_pic.path):
            os.remove(old_pic.path)


@receiver(pre_delete, sender=Entry)
def clear_contestant(sender, instance, using, **kwargs):
    try:
        event = Event.objects.get(
            contestant1=instance.user,
            status=0
        )
        event.contestant1 = None
        event.save()
    except Event.DoesNotExist:
        try:
            event = Event.objects.get(
                contestant2=instance.user,
                status=0
            )
            event.contestant2 = None
            event.save()
        except Event.DoesNotExist:
            return False


@receiver(pre_save, sender=Entry)
def send_entry_notification(sender, instance, **kwargs):
    try:
        old_status = Entry.objects.get(pk=instance.pk).entry_status
    except Entry.DoesNotExist:
        return False
    new_status = instance.entry_status
    if old_status != new_status:
        if new_status == 1:
            status = " has been rejected"
        elif new_status == 2:
            status = " has been accepted"

        subject = instance.event.event_name + " Entry Status"
        body = "Your entry to " + instance.event.event_name + status + "."
        send_entry_notification_email.delay(instance.user.pk, subject, body)
