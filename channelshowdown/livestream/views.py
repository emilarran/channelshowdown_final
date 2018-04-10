# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from opentok import OpenTok, Roles, MediaModes
from django.views.generic import View
from django.http import (
    JsonResponse,
    HttpResponseBadRequest
)
from django.contrib.auth.models import User
from .models import Episode, Viewer
from event.models import Event
from django.conf import settings


# Create your views here.


api_key = settings.API_KEY
api_secret = settings.API_SECRET
opentok = OpenTok(api_key, api_secret)


@method_decorator(csrf_exempt, name='dispatch')
class StartLiveStreamView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        context = {}
        if event.status == 1:
            try:
                session_id = event.episode.session_id
                views = event.episode.views
                token = opentok.generate_token(
                    session_id,
                    role=Roles.publisher
                )
                context = {
                    'event_id': event.id,
                    'session_id': session_id,
                    'token': token,
                    'views': views,
                    'api_key': api_key
                }
            except Episode.DoesNotExist:
                session = opentok.create_session(media_mode=MediaModes.routed)
                episode = Episode(
                    event=event,
                    session_id=session.session_id
                )
                episode.save()
                token = opentok.generate_token(
                    session.session_id,
                    role=Roles.publisher
                )
                context = {
                    'event_id': event.id,
                    'session_id': session.session_id,
                    'token': token,
                    'views': episode.views,
                    'api_key': api_key
                }
            return JsonResponse(context)
        elif event.status == 0:
            return HttpResponseBadRequest("This event is not yet live.")
        else:
            return HttpResponseBadRequest("This event is finished.")


@method_decorator(csrf_exempt, name='dispatch')
class GetTokenPublisherView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        if event.status == 1:
            try:
                session_id = event.episode.session_id
                token = opentok.generate_token(
                    session_id,
                    role=Roles.publisher
                )
                context = {
                    'event_id': event.id,
                    'session_id': session_id,
                    'token': token,
                    'api_key': api_key,
                }
                return JsonResponse(context)
            except Episode.DoesNotExist:
                return HttpResponseBadRequest(
                    "Livestream hasn't been started by creator yet"
                )
        elif event.status == 0:
            return HttpResponseBadRequest("This event is not yet live.")
        else:
            return HttpResponseBadRequest("This event is finished.")


@method_decorator(csrf_exempt, name='dispatch')
class GetTokenSubscriberView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        user = User.objects.get(username=username)
        if event.status == 1:
            try:
                session_id = event.episode.session_id
                token = opentok.generate_token(
                    session_id,
                    role=Roles.subscriber
                )
                try:
                    viewer = Viewer.objects.get(
                        episode=event.episode,
                        user=user
                    )
                except Viewer.DoesNotExist:
                    viewer = Viewer(episode=event.episode, user=user)
                    event.episode.views = event.episode.views + 1
                    viewer.save()

                context = {
                    'event_id': event.id,
                    'session_id': session_id,
                    'token': token,
                    'api_key': api_key,
                }
                return JsonResponse(context)
            except Episode.DoesNotExist:
                return HttpResponseBadRequest(
                    "Livestream hasn't been started by creator yet"
                )
        elif event.status == 0:
            return HttpResponseBadRequest("This event is not yet live.")
        else:
            return HttpResponseBadRequest("This event is finished.")


@method_decorator(csrf_exempt, name='dispatch')
class VoteView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        contestant = request.POST.get('contestant', None)
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        user = User.objects.get(username=username)
        viewer = Viewer.objects.get(user=user)
        if viewer.has_voted == 0:
            if event.contestant1 is contestant:
                event.votes_contestant1 = event.votes_contestant1 + 1
            else:
                event.votes_contestant2 = event.votes_contestant2 + 1

            viewer.has_voted = 1
            viewer.save()
            context = {
                'status': "Vote successful"
            }
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest("You have already voted")


@method_decorator(csrf_exempt, name='dispatch')
class StartArchiveView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        archive = opentok.start_archive(
            event.episode.session_id,
            name=unicode(event.event_name)
        )
        event.episode.archive_id = archive.id
        event.episode.save()
        context = {
            'status': "Archive started."
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class StopArchiveView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        archive_id = event.episode.archive_id
        opentok.stop_archive(archive_id)
        context = {
            'status': "Archive stopped."
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class EndEventView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        if event.status == 1:
            event.status = 2
            event.save()
            context = {
                'status': "Event ended."
            }
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest("Invalid")
