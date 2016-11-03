# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20160824_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_description',
            field=models.TextField(blank=True, help_text='Text to display on your profile', null=True, verbose_name='Profile text'),
        ),
    ]