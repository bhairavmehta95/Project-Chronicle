# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speech', '0005_auto_20160802_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_subject',
            field=models.CharField(default=b'QUESTION', max_length=100),
        ),
    ]
