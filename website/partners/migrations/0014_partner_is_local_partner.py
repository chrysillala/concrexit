# Generated by Django 2.2.1 on 2019-06-07 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0013_auto_20181107_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='is_local_partner',
            field=models.BooleanField(default=False),
        ),
    ]