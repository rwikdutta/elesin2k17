# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 22:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Compliments', '0010_departments_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departments',
            name='timestamp',
        ),
    ]