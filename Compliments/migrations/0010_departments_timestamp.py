# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compliments', '0009_messages_deleted_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]