# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event, Entry
import datetime
# Create your views here.


class CreateEventView(View):
    def post(self, request, **kwargs):
        context = {}
        event_name = request.POST.get('event_name', None)
        date_created = timezone.now()
        date_event = request.POST.get('date_event', None).isoformat()
        creator = request.user.id
        status = 0
        event = Event(event_name=event_name,
                      date_created=date_created,
                      date_event=date_event,
                      creator=creator,
                      status=status)
        event.save()
        context['status'] = "created"
        return JsonResponse(context)


class SendEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        event_id = request.POST.get('event_id', None)
        username = request.POST.get('username', None)
        user = User.objects.get(username=username)
        entry = Entry(event_id=event_id,
                      user_id=user.id,
                      entry_status=0)
        entry.save()
        context['status'] = "created"
        return JsonResponse(context)
