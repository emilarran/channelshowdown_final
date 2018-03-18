# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from event.models import Event

# Create your models here.


class Episode(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='episodes')
    session_id = models.CharField(max_length=200)
    archive_id = models.CharField(max_length=200)
