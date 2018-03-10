# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserInfo
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):
    def post(self, request, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # User.objects.create(username=username, password=password, email=email)
        # user = authenticate(request, username=username, password=password)
        import pdb; pdb.set_trace()
        user, created = User.objects.get_or_create(username=username)
        context = {
            'username': username,
            'password': password,
            'email': email,
        }
        if created:
            user.set_password(password)
            user.save()
            if request.POST['userType'] == "normal":
                userinfo = UserInfo(user_id=user.id, user_type="normal")
                userinfo.save()
            # login(request, user)
            context['status'] = "registered"
            return JsonResponse(context)
        else:
            context['status'] = "not registered"
            return JsonResponse(context)
