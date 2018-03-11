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
    def get(self, request, **kwargs):
        event_name = request.POST.get('event_name', None)
        date_created = timezone.now()
        date_event = request.POST.get('date_event', None).isoformat()
        creator = request.user.id
        status = 0

        
