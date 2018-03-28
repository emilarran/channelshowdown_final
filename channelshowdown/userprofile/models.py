
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

USER_TYPE = (
    (0, 'normal'),
    (1, 'commentator')
)


class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='userinfo')
    profile_pic = models.ImageField(
        upload_to='profile_image/',
        default='profile_image/default_profpic.png',
        # blank=True,
        # null=True,
        # default=None
    )
    # user_type = models.CharField(max_length=50)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=0)
    user_video = models.FileField(
        upload_to='profile_video/',
        default='profile_video/default_video.mp4',
        # blank=True,
        # null=True,
        # # default=None
    )
    video_thumbnail = models.ImageField(
        upload_to='video_thumbnail/',
        default='video_thumbnail/default_thumbnail.png',
        # blank=True,
        # null=True,
        # # default=None
    )
    bio = models.CharField(max_length=120, default="", blank=True)
