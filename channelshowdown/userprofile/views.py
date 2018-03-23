# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserInfo
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        # password = request.POST['password']
        # email = request.POST['email']
        # User.objects.create(username=username, password=password, email=email)
        # user = authenticate(request, username=username, password=password)
        user, created = User.objects.get_or_create(username=username)
        context = {
            'username': username,
            'email': email,
        }
        if created:
            user.set_password(password)
            user.email = email
            user.save()
            context['user_id'] = user.id
            if request.POST.get('userType', None) == "normal":
                userinfo = UserInfo(user_id=user.id, user_type=0)
                userinfo.save()
            elif request.POST.get('userType', None) == "commentator":
                userinfo = UserInfo(user_id=user.id, user_type=1)
                userinfo.save()
            context['status'] = "registered"
            return JsonResponse(context)
        else:
            context['status'] = "username already taken"
            return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            userinfo = UserInfo.objects.get(user=user.id)
            context = {
                'username': user.username,
                'email': user.email,
                'userType': userinfo.user_type,
                'session_key': request.session.session_key,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'bio': userinfo.bio,
            }
            return JsonResponse(context)
        else:
            return HttpResponseNotFound("Login failed")


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request, **kwargs):
        logout(request)
        context = {'status': "logged out"}
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class EditUserView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        bio = request.POST.get('bio', None)
        firstname = request.POST.get('firstName', None)
        lastname = request.POST.get('lastName', None)
        user = User.objects.get(username=username)
        userinfo = UserInfo.objects.get(user=user.id)
        userinfo.bio = bio
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        userinfo.save()
        context = {
            'bio': bio,
            'firstName': firstname,
            'lastName': lastname,
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        try:
            user = User.objects.get(username=username)
            userinfo = userinfo = UserInfo.objects.get(user=user.id)
            context = {
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'bio': userinfo.bio,
            }
            return JsonResponse(context)
        except User.DoesNotExist:
            return HttpResponseNotFound("User not found")



# @method_decorator(csrf_exempt, name='dispatch')
# class UploadVideoView(View)