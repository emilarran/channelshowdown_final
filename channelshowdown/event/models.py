# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

EVENT_STATUS = (
    (0, 'Upcoming'),
    (1, 'Ongoing'),
    (2, 'Finished'),
    (3, 'Canceled')
)

ENTRY_STATUS = (
    (0, 'Pending'),
    (1, 'Rejected'),
    (2, 'Accepted')
)

VOTING_STATUS = (
    (0, 'Open'),
    (1, 'Closed')
)


class Event(models.Model):
    event_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    prize = models.CharField(max_length=100, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_event = models.DateTimeField(blank=False, null=False)
    creator = models.ForeignKey(User, related_name='event_creator')
    contestant1 = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='event_contestant1',
                                    default="")
    contestant2 = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='event_contestant2',
                                    default="")
    votes_contestant1 = models.PositiveIntegerField(default=0)
    votes_contestant2 = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=EVENT_STATUS, default=0)
    event_image = models.ImageField(
        upload_to='event_image/',
        default='event_image/default.jpg',
    )
    voting_status = models.PositiveSmallIntegerField(
        choices=VOTING_STATUS,
        default=0
    )
    date_ended = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.event_name


class Entry(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='entries')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entries')
    entry_status = models.PositiveSmallIntegerField(
        choices=ENTRY_STATUS,
        default=0)
