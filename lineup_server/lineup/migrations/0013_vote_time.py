# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-13 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0012_auto_20161022_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='time',
            field=models.CharField(default='', max_length=100),
        ),
    ]
