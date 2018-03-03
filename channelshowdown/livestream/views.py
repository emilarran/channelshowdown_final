# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from opentok import OpenTok, Roles, MediaModes
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import json

# Create your views here.


api_key = "46071272"
api_secret = "54cb69236b6eabe260ff578144e5e4f31e3c7054"
opentok = OpenTok(api_key,api_secret) 

class StartLiveStreamView(View):
    def get(self, request, **kwargs):
        session = opentok.create_session(media_mode=MediaModes.routed)
        print(session)
        import pdb; pdb.set_trace()

        return HttpResponse(json.dumps(session.session_id),'text/json')


class GetToken(View):
    def get(self, request, **kwargs):
        

