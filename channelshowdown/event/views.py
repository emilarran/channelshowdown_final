# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Event, Entry
import datetime
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CreateEventView(View):
    def post(self, request, **kwargs):
        context = {}
        event_name = request.POST.get('eventName', None)
        description = request.POST.get('eventDescription', None)
        date_created = timezone.now()
        date_event = parse_datetime(request.POST.get('eventDate', None))
        creator = request.POST.get('username', None)
        prize = request.POST.get('prize', None)
        # creator = request.user.id
        status = 0
        event = Event(event_name=event_name,
                      description=description,
                      date_created=date_created,
                      date_event=date_event,
                      creator=creator,
                      prize=prize,
                      status=status)
        event.save()
        context['status'] = "created"
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
class AllEntriesView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        entries = Entry.objects.filter(event_id=event_id)
        context = {
            'entry': entries
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class ApproveEntryView(View):
    def post(self, request, **kwargs):
        entry_id = request.POST.get('entry_id', None)
        entry = Entry.objects.get(id=entry_id)
        event = Event.objects.get(id=entry.event.id)
        if event.contestant1:
            return JsonResponse(context)