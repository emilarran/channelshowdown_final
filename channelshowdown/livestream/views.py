# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from opentok import OpenTok, Roles, MediaModes, OutputModes
from django.views.generic import View
from django.http import (
    JsonResponse,
    HttpResponseBadRequest
)
from django.utils import timezone
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
        if event.status == 1 and event.contestant1 is not None and event.contestant2 is not None:
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
        elif event.contestant1 is None or event.contestant2 is None:
            message = ""
            if event.contestant1 is None:
                message = message + "Lacking contestant 1. "
            if event.contestant2 is None:
                message = message + "Lacking contestant 2."
            print(message)
            return HttpResponseBadRequest(message)
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
                    event.episode.save()

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
        contestant_name = request.POST.get('contestant', None)
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        user = User.objects.get(username=username)
        contestant = User.objects.get(username=contestant_name)
        viewer = Viewer.objects.get(user=user)
        if viewer.has_voted == 0 and event.voting_status == 0:
            if event.contestant1 == contestant:
                event.votes_contestant1 = event.votes_contestant1 + 1
            else:
                event.votes_contestant2 = event.votes_contestant2 + 1

            viewer.has_voted = 1
            event.save()
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

        if event.episode.archive_id is None:
            archive = opentok.start_archive(
                event.episode.session_id,
                name=unicode(event.event_name),
                output_mode=OutputModes.composed
            )
            event.episode.archive_id = archive.id
            event.episode.save()
            context = {
                'status': "Archive started."
            }
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest("Archive already started.")


@method_decorator(csrf_exempt, name='dispatch')
class EndEventView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        if event.status == 1:
            archive_id = event.episode.archive_id
            opentok.stop_archive(archive_id)
            event.status = 2
            event.date_ended = timezone.now()
            event.save()
            context = {
                'status': "Event ended. Archive stopped."
            }
            return JsonResponse(context)
        else:
            return HttpResponseBadRequest("Invalid")


@method_decorator(csrf_exempt, name='dispatch')
class SavedVideoView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id')
        event = Event.objects.get(pk=event_id)
        archive_id = event.episode.archive_id
        archive = opentok.get_archive(archive_id)
        video = archive.url
        event.episode.views = event.episode.views + 1
        event.episode.save()
        context = {
            'video': video
        }
        return JsonResponse(context)
