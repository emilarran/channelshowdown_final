# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest
)
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.forms.models import model_to_dict
from django.conf import settings
from .models import Event, Entry
from .forms import EventCreationForm
import pytz


@method_decorator(csrf_exempt, name='dispatch')
class CreateEventView(View):
    def post(self, request, **kwargs):
        form = EventCreationForm(request.POST)
        if form.is_valid():
            return form.save()
        else:
            message = "Error: "
            for error in form.errors:
                message = message + form.errors[error][0] + " "
                print(message)
            return HttpResponseBadRequest(message)


@method_decorator(csrf_exempt, name='dispatch')
class SendEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        event_id = request.POST.get('event_id', None)
        username = request.POST.get('username', None)
        user = User.objects.get(username=username)
        entry, created = Entry.objects.get_or_create(event_id=event_id,
                                                     user_id=user.id,)
        if created:
            context['status'] = "Entry sent"
            entry.save()
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest("You have already sent your entry")


@method_decorator(csrf_exempt, name='dispatch')
class AllEntriesView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        entries = list(Entry.objects.filter(event_id=event_id).values())
        for entry in entries:
            entry['username'] = User.objects.get(pk=entry['user_id']).username
        context = {
            'entries': entries
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class UpcomingEventsView(View):
    def post(self, request, **kwargs):
        timezone = request.POST.get('timezone', None)
        timezone = pytz.timezone(timezone)
        events = list(Event.objects.filter(status=0).values())
        context = {
            'events': events
        }
        for event in context['events']:
            event['date_event'] = event['date_event'].astimezone(timezone)
            event['date_event'] = event['date_event'].replace(tzinfo=None)
            event['event_image'] = settings.MEDIA_URL + event['event_image']
            user = User.objects.get(pk=event['creator_id'])
            event['creator_name'] = user.username
            if event['contestant1_id'] is not None:
                user = User.objects.get(pk=event['contestant1_id'])
                event['contestant1_name'] = user.username
            else:
                event['contestant1_name'] = ""
            if event['contestant2_id'] is not None:
                user = User.objects.get(pk=event['contestant2_id'])
                event['contestant2_name'] = user.username
            else:
                event['contestant2_name'] = ""
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class OngoingEventsView(View):
    def post(self, request, **kwargs):
        timezone = request.POST.get('timezone', None)
        timezone = pytz.timezone(timezone)
        events = list(Event.objects.filter(status=1).values())
        context = {
            'events': events
        }
        for event in context['events']:
            event['date_event'] = event['date_event'].astimezone(timezone)
            event['date_event'] = event['date_event'].replace(tzinfo=None)
            event['event_image'] = settings.MEDIA_URL + event['event_image']
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class FinishedEventsView(View):
    def post(self, request, **kwargs):
        timezone = request.POST.get('timezone', None)
        timezone = pytz.timezone(timezone)
        events = list(Event.objects.filter(status=2).values())
        context = {
            'events': events
        }
        for event in context['events']:
            event['date_event'] = event['date_event'].astimezone(timezone)
            event['date_event'] = event['date_event'].replace(tzinfo=None)
            event['event_image'] = settings.MEDIA_URL + event['event_image']
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class ApproveEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        entry_id = request.POST.get('entry_id', None)
        try:
            entry = Entry.objects.get(id=entry_id)
            event = Event.objects.get(id=entry.event.id)
        except Entry.DoesNotExist:
            return HttpResponseNotFound("Entry does not exist.")
        except Event.DoesNotExist:
            return HttpResponseNotFound("Event not found.")

        if entry.entry_status != 2:
            if not event.contestant1:
                event.contestant1 = entry.user
                entry.entry_status = 2
                entry.save()
                event.save()
                context['status'] = "Approved"
                return JsonResponse(context)
            elif not event.contestant2:
                event.contestant2 = entry.user
                entry.entry_status = 2
                entry.save()
                event.save()
                context['status'] = "Approved"
                return JsonResponse(context)
            else:
                return HttpResponseNotFound("Cannot approve entry")
        else:
            return HttpResponseNotFound("Entry already approved")


@method_decorator(csrf_exempt, name='dispatch')
class RejectEntryView(View):
    def post(self, request, **kwargs):
        context = {}
        entry_id = request.POST.get('entry_id', None)
        try:
            entry = Entry.objects.get(id=entry_id)
            event = Event.objects.get(id=entry.event.id)
        except Entry.DoesNotExist:
            return HttpResponseNotFound("Entry does not exist.")
        except Event.DoesNotExist:
            return HttpResponseNotFound("Event not found.")

        if event.contestant1_id == entry.user_id:
            event.contestant1 = None
        else:
            event.contestant2 = None
        entry.entry_status = 1
        entry.save()
        event.save()
        context['status'] = "Rejected"
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class CreatorEventProfileView(View):
    def post(self, request, **kwargs):
        timezone = request.POST.get('timezone', None)
        timezone = pytz.timezone(timezone)
        username = request.POST.get('username', None)
        user = User.objects.get(username=username)
        try:
            event = Event.objects.get(
                creator_id=user.id,
                status__lte=1,
                status__gte=0)
        except Event.DoesNotExist:
            return HttpResponseNotFound("You have no events at the moment.")
        eventdict = model_to_dict(event)
        eventdict['event_image'] = eventdict['event_image'].url
        eventdict['date_event'] = eventdict['date_event'].astimezone(timezone)
        eventdict['date_event'] = eventdict['date_event'].replace(tzinfo=None)
        eventdict['creator_name'] = event.creator.username
        if eventdict['contestant1'] is not None:
            user = User.objects.get(pk=eventdict['contestant1'])
            eventdict['contestant1_name'] = user.username
        else:
            eventdict['contestant1_name'] = ""
        if eventdict['contestant2'] is not None:
            user = User.objects.get(pk=eventdict['contestant2'])
            eventdict['contestant2_name'] = user.username
        else:
            eventdict['contestant2_name'] = ""
        context = {
            'event': eventdict
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class EventProfileView(View):
    def post(self, request, **kwargs):
        timezone = request.POST.get('timezone', None)
        timezone = pytz.timezone(timezone)
        event_id = request.POST.get('event_id', None)
        event = model_to_dict(Event.objects.get(id=event_id))
        event['date_event'] = event['date_event'].astimezone(timezone)
        event['date_event'] = event['date_event'].replace(tzinfo=None)
        event['event_image'] = settings.MEDIA_URL + event['event_image']
        context = {
            'event': event
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class UploadEventImageView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        image = request.FILES['image']
        image_types = [
            'image/png',
            'image/jpg',
            'image/jpeg',
            'image/pjpeg'
        ]
        if image.content_type not in image_types:
            return HttpResponseBadRequest("Invalid image file format")

        if image.content_type == u'image/png':
            image.name = event.event_name + u'.png'
        elif image.content_type == u'image/jpg':
            image.name = event.event_name + u'.jpg'
        elif image.content_type == u'image/jpeg':
            image.name = event.event_name + u'.jpeg'
        elif image.content_type == u'image/pjpeg':
            image.name = event.event_name + u'.pjpeg'

        # image.name = username
        event.event_image = image
        event.save()
        context = {
            'status': "Event image successfully uploaded.",
            'event_image': event.event_image.url,
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class MyEventView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        user = User.objects.get(username=username)
        timezone = request.POST.get('timezone', None)
        timezone = pytz.timezone(timezone)
        try:
            event = Event.objects.get(
                contestant1=user,
                status__gte=0,
                status__lte=1
            )
        except Event.DoesNotExist:
            try:
                event = Event.objects.get(
                    contestant2=user,
                    status__gte=0,
                    status__lte=1
                )
            except Event.DoesNotExist:
                return HttpResponseBadRequest(
                    "You do not have an event right now"
                )
        eventdict = model_to_dict(event)
        eventdict['event_image'] = eventdict['event_image'].url
        eventdict['date_event'] = eventdict['date_event'].astimezone(timezone)
        eventdict['date_event'] = eventdict['date_event'].replace(tzinfo=None)
        eventdict['creator_name'] = event.creator.username
        if eventdict['contestant1'] is not None:
            user = User.objects.get(pk=eventdict['contestant1'])
            eventdict['contestant1_name'] = user.username
        else:
            eventdict['contestant1_name'] = ""
        if eventdict['contestant2'] is not None:
            user = User.objects.get(pk=eventdict['contestant2'])
            eventdict['contestant2_name'] = user.username
        else:
            eventdict['contestant2_name'] = ""
        context = {
            'event': eventdict
        }
        return JsonResponse(context)


# @method_decorator(csrf_exempt, name='dispatch')
# class ChangeEventStatusView(View):
#     def post(self, request, **kwargs):
#         event 


# @method_decorator(csrf_exempt, name='dispatch')
# class
