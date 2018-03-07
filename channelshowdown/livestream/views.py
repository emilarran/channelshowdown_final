# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from opentok import OpenTok, Roles, MediaModes
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.


api_key = "46071272"
api_secret = "54cb69236b6eabe260ff578144e5e4f31e3c7054"
opentok = OpenTok(api_key, api_secret)


class StartLiveStreamView(View):
    def get(self, request, **kwargs):
        session = opentok.create_session(media_mode=MediaModes.routed)
        token = opentok.generate_token(session.session_id, role=Roles.moderator)
        context = {
            'session_id': session.session_id,
            'token_id': token
        }
        # return HttpResponse(json.dumps(session.session_id), 'text/json')
        return JsonResponse(context)


class GetTokenPublisher(View):
    def get(self, request, **kwargs):
        session = request.GET['session_id']
        token = opentok.generate_token(session, role=Roles.publisher)
        context = {'token_id': token}
        return JsonResponse(context)


class GetTokenSubscriber(View):
    def get(self, request, **kwargs):
        session = request.GET['session_id']
        token = opentok.generate_token(session, role=Roles.subscriber)
        context = {'token_id': token}
        return JsonResponse(context)
