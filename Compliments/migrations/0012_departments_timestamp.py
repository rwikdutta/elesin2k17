# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compliments', '0011_remove_departments_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]