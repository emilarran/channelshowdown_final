from django.contrib.auth.models import User
from .models import UserInfo
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import os


@receiver(pre_save, sender=UserInfo)
def delete_unused_userinfo_file(sender, instance, **kwargs):
    # import pdb; pdb.set_trace()
    if not instance.pk:
        return False
    try:
        old_pic = UserInfo.objects.get(pk=instance.pk).profile_pic
        old_vid = UserInfo.objects.get(pk=instance.pk).user_video
        old_thumb = UserInfo.objects.get(pk=instance.pk).video_thumbnail
    except UserInfo.DoesNotExist:
        return False

    new_pic = instance.profile_pic
    new_vid = instance.user_video
    new_thumb = instance.video_thumbnail
    if (not old_pic == new_pic) & (not old_pic.url == '/media/profile_image/default_profpic.png'):
        if os.path.isfile(old_pic.path):
            os.remove(old_pic.path)
    if (not old_vid == new_vid) & (not old_vid.url == '/media/profile_video/default_video.mp4'):
        if os.path.isfile(old_vid.path):
            os.remove(old_vid.path)
    if (not old_thumb == new_thumb) & (not old_thumb.url == '/media/video_thumbnail/default_thumbnail.png'):
        if os.path.isfile(old_thumb.path):
            os.remove(old_thumb.path)


@receiver(post_save, sender=User)
def create_additional_user_data(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
