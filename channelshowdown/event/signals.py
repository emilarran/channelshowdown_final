from .models import Event
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os


@receiver(pre_save, sender=Event)
def delete_unused_eventinfo_file(sender, instance, **kwargs):
    # import pdb; pdb.set_trace()
    if not instance.pk:
        return False
    try:
        old_pic = Event.objects.get(pk=instance.pk).event_image
    except Event.DoesNotExist:
        return False

    new_pic = instance.profile_pic
    if (not old_pic == new_pic) & (not old_pic.url == '/media/profile_image/default.jpg'):
        if os.path.isfile(old_pic.path):
            os.remove(old_pic.path)
