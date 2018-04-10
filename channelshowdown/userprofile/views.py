# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserInfo, Device
# from .forms import FileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import RegistrationForm, EditUserForm


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):
    def post(self, request, **kwargs):
        context = {
            'username': request.POST.get('username', None),
            'email': request.POST.get('email', None),
        }
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(
                username=request.POST.get('username', None)
            )
            userinfo = UserInfo.objects.get(
                user=request.POST.get('user', user)
            )
            if request.POST.get('userType', None) == "normal":
                userinfo.user_type = 0
                userinfo.save()
            elif request.POST.get('userType', None) == "commentator":
                userinfo.user_type = 1
                userinfo.save()
            context['status'] = "registered"
            return JsonResponse(context)
        else:
            message = "Error: "
            for error in form.errors:
                message = message + form.errors[error][0] + " "
            print message
            return HttpResponseBadRequest("message")


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # device_id = request.POST.get('device_id', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context = {
                'username': user.username,
                'email': user.email,
                'userType': user.userinfo.user_type,
                'session_key': request.session.session_key,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'bio': user.userinfo.bio,
            }
            # device_check = Device.objects.filter(
            #     device_id=device_id,
            #     is_active=1
            # )
            # for device in device_check:
            #     device.is_active = 0
            #     device.save()
            # device, created = Device.objects.get_or_create(
            #     user=user,
            #     device_id=device_id
            # )
            # if created:
            #     device.save()
            # else:
            #     device.is_active = 1
            #     device.save()

            if not user.userinfo.user_video:
                context['user_video'] = '/media/profile_video/default_video.mp4'
            else:
                context['user_video'] = user.userinfo.user_video.url
            if not user.userinfo.profile_pic:
                context['profile_pic'] = '/media/profile_video/default_profpic.png'
            else:
                context['profile_pic'] = user.userinfo.profile_pic.url
            if not user.userinfo.user_video:
                context['video_thumbnail'] = '/media/profile_video/default_thumbnail.png'
            else:
                context['video_thumbnail'] = user.userinfo.video_thumbnail.url
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
        form = EditUserForm(request.POST)
        if form.is_valid():
            form.save()
            bio = request.POST.get('bio', None)
            firstname = request.POST.get('firstName', None)
            lastname = request.POST.get('lastName', None)
            context = {
                'bio': bio,
                'firstName': firstname,
                'lastName': lastname,
            }
            # user = User.objects.get(username=username)
            # user.userinfo.bio = bio
            # user.first_name = firstname
            # user.last_name = lastname
            # user.save()
            # user.userinfo.save()
            # context = {
            #     'bio': bio,
            #     'firstName': firstname,
            #     'lastName': lastname,
            # }
            return JsonResponse(context)
        else:
            message = "Error: "
            for error in form.errors:
                message = message + form.errors[error][0] + " "
            print message
            return HttpResponseBadRequest(message)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username', None)
        try:
            user = User.objects.get(username=username)
            context = {
                'username': user.username,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'bio': user.userinfo.bio,
            }
            if not user.userinfo.user_video:
                context['user_video'] = '/media/profile_video/default_video.mp4'
            else:
                context['user_video'] = user.userinfo.user_video.url
            if not user.userinfo.profile_pic:
                context['profile_pic'] = '/media/profile_video/default_profpic.png'
            else:
                context['profile_pic'] = user.userinfo.profile_pic.url
            if not user.userinfo.user_video:
                context['video_thumbnail'] = '/media/profile_video/default_thumbnail.png'
            else:
                context['video_thumbnail'] = user.userinfo.video_thumbnail.url
            return JsonResponse(context)
        except User.DoesNotExist:
            return HttpResponseNotFound("User not found")


@method_decorator(csrf_exempt, name='dispatch')
class UploadProfPicView(View):
    def post(self, request, **kwargs):
        context = {}
        username = request.POST.get('username')
        file = request.FILES['image']
        image_types = [
            'image/png',
            'image/jpg',
            'image/jpeg',
            'image/pjpeg'
        ]
        if file.content_type not in image_types:
            return HttpResponseBadRequest("Invalid image file format")

        # file.name = username
        if file.content_type == u'image/png':
            file.name = username + u'.png'
        elif file.content_type == u'image/jpg':
            file.name = username + u'.jpg'
        elif file.content_type == u'image/jpeg':
            file.name = username + u'.jpeg'
        elif file.content_type == u'image/pjpeg':
            file.name = username + u'.pjpeg'

        user = User.objects.get(username=username)
        user.userinfo.profile_pic = file
        user.userinfo.save()
        context = {
            'status': "Image upload successful",
            'profile_pic': user.userinfo.profile_pic.url
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class UploadVideoView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username')
        video = request.FILES['video']
        video_types = [
            'video/avi',
            'video/flv',
            'video/mov',
            'video/wmv',
            'video/mp4'
        ]
        if video.content_type not in video_types:
            return HttpResponseBadRequest("Invalid video file format")

        user = User.objects.get(username=username)
        # video.name = username

        if video.content_type == u'video/avi':
            video.name = username + u'.avi'
        elif video.content_type == u'video/flv':
            video.name = username + u'.flv'
        elif video.content_type == u'video/mov':
            video.name = username + u'.mov'
        elif video.content_type == u'video/wmv':
            video.name = username + u'.wmv'
        elif video.content_type == u'video/mp4':
            video.name = username + u'.mp4'

        user.userinfo.user_video = video
        user.userinfo.save()
        context = {
            'status': "Video upload successful",
            'user_video': user.userinfo.user_video.url,
        }
        return JsonResponse(context)


@method_decorator(csrf_exempt, name='dispatch')
class UploadThumbnailView(View):
    def post(self, request, **kwargs):
        username = request.POST.get('username')
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
            image.name = username + u'.png'
        elif image.content_type == u'image/jpg':
            image.name = username + u'.jpg'
        elif image.content_type == u'image/jpeg':
            image.name = username + u'.jpeg'
        elif image.content_type == u'image/pjpeg':
            image.name = username + u'.pjpeg'

        user = User.objects.get(username=username)
        # image.name = username
        user.userinfo.video_thumbnail = image
        user.userinfo.save()
        context = {
            'status': "Thumbnail upload successful",
            'video_thumbnail': user.userinfo.video_thumbnail.url,
        }
        return JsonResponse(context)
