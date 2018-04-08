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

    # def get(self, request, **kwargs):
    #     session = opentok.create_session(media_mode=MediaModes.routed)
    #     token = opentok.generate_token(session.session_id,
    #                                    role=Roles.moderator)
    #     archive = opentok.start_archive(session.session_id)
    #     episode = Episode(event=request.GET['event'],
    #                       session_id=session,
    #                       archive_id=archive.id)
    #     episode.save()
    #     context = {
    #         'event': request.GET['event'],
    #         'session_id': session.session_id,
    #         'token_id': token,
    #         'archive_id': archive.id
    #     }
    #     return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class GetTokenPublisherView(View):
    def post(self, request, **kwargs):
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
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

    def get(self, request, **kwargs):
        session = request.GET['session_id']
        token = opentok.generate_token(session, role=Roles.publisher)
        context = {'token': token}
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class GetTokenSubscriberView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        event_id = request.POST.get('event_id', None)
        event = Event.objects.get(id=event_id)
        user = User.objects.get(username=username)
        try:
            session_id = event.episode.session_id
            token = opentok.generate_token(
                session_id,
                role=Roles.subscriber
            )
            viewer = Viewer(
                episode=event.episode,
                user=user,
            )
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
