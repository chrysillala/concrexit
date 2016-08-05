# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-07-27 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_squashed_0002_auto_20160707_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='BecomeAMemberDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='members/', validators=[utils.validators.validate_file_extension])),
            ],
        ),
    ]