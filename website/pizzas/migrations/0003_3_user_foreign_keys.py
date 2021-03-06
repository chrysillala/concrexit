# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-12 09:59
from __future__ import unicode_literals

from django.db import migrations


def forward_func(apps, schema_editor):
    Order = apps.get_model('pizzas', 'Order')

    for order in Order.objects.all():
        if order.member_old:
            order.member = order.member_old.user
            order.save(update_fields=('member',))


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0003_2_user_foreign_keys'),
    ]

    operations = [
        migrations.RunPython(
            code=forward_func,
        ),
    ]
