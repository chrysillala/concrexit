# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_photo__digest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]