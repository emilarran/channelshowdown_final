# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from event.models import Event

VOTE_STATUS = (
    (0, 'has_not_voted'),
    (1, 'has_voted')
)


class Episode(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='episode')
    session_id = models.CharField(
        max_length=200,
        default=None,
        null=True,
        blank=True
    )
    archive_id = models.CharField(
        max_length=200,
        default=None,
        null=True,
        blank=True
    )
    views = models.PositiveSmallIntegerField(default=0)


class Viewer(models.Model):
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
        related_name='viewers'
    )
    user = models.ForeignKey(
        User,
        related_name='viewers'
    )
    has_voted = models.PositiveSmallIntegerField(
        choices=VOTE_STATUS,
        default=0
    )
