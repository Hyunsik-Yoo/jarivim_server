# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-18 07:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0003_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='restaurant_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='bob', max_length=100)),
                ('title', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='vote',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 18, 7, 55, 37, 279253)),
        ),
    ]
