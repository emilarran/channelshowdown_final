from django import forms
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.dateparse import parse_datetime
from django.conf import settings
import pytz
from .models import Event


class EventCreationForm(forms.Form):
    eventName = forms.CharField()
    eventDescription = forms.CharField()
    prize = forms.CharField()
    username = forms.CharField()
    eventDate = forms.CharField()
    timezone = forms.CharField()

    def save(self, *args, **kwargs):
        context = {}
        username = self.cleaned_data['username']
        event_name = self.cleaned_data['eventName']
        description = self.cleaned_data['eventDescription']
        prize = self.cleaned_data['prize']
        date_event = self.cleaned_data['eventDate']
        timezone = self.cleaned_data['timezone']
        print(timezone)
        try:
            date_event = parse_datetime(date_event)
        except Exception:
            return HttpResponseBadRequest(
                "Invalid date-time"
            )
        date_event = date_event.replace(tzinfo=pytz.timezone(timezone))
        tz = pytz.timezone(settings.TIME_ZONE)
        date_event = date_event.astimezone(tz)
        user = User.objects.get(username=username)
        try:
            event = Event.objects.get(
                creator_id=user.id,
                status__gte=0,
                status__lte=1
            )
            return HttpResponseBadRequest(
                "You already have an upcoming or ongoing event."
            )
        except Exception:
            event = Event(
                event_name=event_name,
                description=description,
                date_event=date_event,
                creator=user,
                prize=prize
            )
            event.save()
            context['status'] = "created"
            return JsonResponse(context)
