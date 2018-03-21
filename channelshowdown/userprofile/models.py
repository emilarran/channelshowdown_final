
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

USER_TYPE = (
    (0, 'normal'),
    (1, 'commentator')
)


class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='userinfo')
    profile_pic = models.ImageField()
    # user_type = models.CharField(max_length=50)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=0)
    user_video = models.FileField(upload_to='uploads/')
    bio = models.CharField(max_length=120)
