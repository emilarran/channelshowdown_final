# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

EVENT_STATUS = (
    (0, 'Upcoming'),
    (1, 'Ongoing'),
    (2, 'Finished')
)

ENTRY_STATUS = (
    (0, 'Pending'),
    (1, 'Rejected'),
    (2, 'Accepted')
)


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    prize = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    date_event = models.DateTimeField()
    creator = models.ForeignKey(User, related_name='event_creator')
    contestant1 = models.ForeignKey(User, related_name='event_contestant1')
    contestant2 = models.ForeignKey(User, related_name='event_contestant2')
    votes_contestant1 = models.PositiveIntegerField(default=0)
    votes_contestant2 = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=EVENT_STATUS, default=0)

    def __str__(self):
        return self.event_name


class Entry(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='entry')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entry')
    entry_status = models.PositiveSmallIntegerField(
        choices=ENTRY_STATUS,
        default=0)
