# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserInfo, Notification
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Notification)