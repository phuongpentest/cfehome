# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-15 17:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20170715_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantlocation',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]