# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0019_auto_20180328_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='video_thumbnail',
            field=models.ImageField(default='video_thumbnail/default_thumbnail.png', upload_to='video_thumbnail/'),
        ),
    ]
