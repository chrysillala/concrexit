# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-07-23 10:47
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationDocumentsYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1990)])),
                ('policy_document', models.FileField(blank=True, upload_to='documents/association/', validators=[utils.validators.validate_file_extension])),
                ('annual_report', models.FileField(blank=True, upload_to='documents/association/', validators=[utils.validators.validate_file_extension])),
                ('financial_report', models.FileField(blank=True, upload_to='documents/association/', validators=[utils.validators.validate_file_extension])),
            ],
        ),
        migrations.DeleteModel(
            name='AssociationDocument',
        ),
    ]