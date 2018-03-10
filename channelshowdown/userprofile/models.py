# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=50)
    user_video = models.FileField(upload_to='uploads/')
    bio = models.CharField(max_length=100)
