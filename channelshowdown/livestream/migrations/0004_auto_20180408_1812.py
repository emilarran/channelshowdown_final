# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-08 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livestream', '0003_auto_20180408_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='event.Event'),
        ),
    ]
