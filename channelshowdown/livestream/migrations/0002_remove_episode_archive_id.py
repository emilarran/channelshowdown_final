# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 13:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livestream', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='archive_id',
        ),
    ]