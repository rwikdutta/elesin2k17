# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compliments', '0003_auto_20170822_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachers',
            name='abbr',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
