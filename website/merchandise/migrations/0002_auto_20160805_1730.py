# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchandiseitem',
            name='image',
            field=models.ImageField(upload_to='public/merchandise'),
        ),
    ]