# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-21 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_1_registration_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='paid'
        )
    ]
