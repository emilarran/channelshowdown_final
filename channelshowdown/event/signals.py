from .models import Event, Entry
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from event.tasks import (
    send_entry_notification_email
)
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
            if old_status == 2:
                if instance.event.contestant1 is instance.user:
                    instance.event.contestant1 = ""
                    instance.event.save()
                elif instance.event.contestant2 is instance.user:
                    instance.event.contestant2 = ""
                    instance.event.save()
        elif new_status == 2:
            status = " has been accepted"
        else:
            status = " is being reviewed"
            if old_status == 2:
                if instance.event.contestant1 is instance.user:
                    instance.event.contestant1 = ""
                    instance.event.save()
                elif instance.event.contestant2 is instance.user:
                    instance.event.contestant2 = ""
                    instance.event.save()
        subject = instance.event.event_name + " Entry Status"
        body = "Your entry to " + instance.event.event_name + status + "."
        send_entry_notification_email.delay(instance.user.pk, subject, body)


@receiver(pre_save, sender=Event)
def send_results_email(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_voting_status = Event.objects.get(pk=instance.pk).voting_status
    except Event.DoesNotExist:
        return False
    new_voting_status = instance.voting_status

    subject = instance.event_name + " Results"
    winner_body = "Congratulations, you have won!"
    loser_body = "Sorry, you lost."
    draw_body = "It was a draw."
    creator_id = instance.creator_id
    if new_voting_status != old_voting_status and new_voting_status == 1:
        if instance.votes_contestant1 > instance.votes_contestant2:
            winner_id = instance.contestant1_id
            loser_id = instance.contestant2_id
            body = "Winner: " + instance.contestant1.username + "\nLoser: " + instance.contestant2.username
        elif instance.votes_contestant2 > instance.votes_contestant1:
            winner_id = instance.contestant2_id
            loser_id = instance.contestant1_id
            body = "Winner: " + instance.contestant2.username + "\nLoser: " + instance.contestant1.username
        else:
            body = winner_body = loser_body = draw_body

        send_entry_notification_email.delay(
            winner_id,
            subject,
            winner_body
        )
        send_entry_notification_email.delay(
            loser_id,
            subject,
            loser_body
        )
        send_entry_notification_email.delay(
            creator_id,
            subject,
            body
        )
