# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-10 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_auto_20160809_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]