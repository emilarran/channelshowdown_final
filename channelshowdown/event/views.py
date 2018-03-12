# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from .models import Event
from django.utils import timezone
import datetime
# Create your views here.


class CreateEvent(View):
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
