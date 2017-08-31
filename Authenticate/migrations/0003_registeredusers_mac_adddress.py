# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 06:06
from __future__ import unicode_literals

import Authenticate.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authenticate', '0002_auto_20170825_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredusers',
            name='mac_adddress',
            field=models.CharField(default='AABBCCDDEEFF', max_length=12, validators=[Authenticate.models.RegisteredUsers.validity_mac]),
            preserve_default=False,
        ),
    ]