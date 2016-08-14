# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speech', '0015_auto_20160813_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollments',
            name='class_id',
            field=models.ForeignKey(default=-1, to='speech.Class'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollments',
            name='student_id',
            field=models.ForeignKey(default=-1, to='speech.Student'),
            preserve_default=False,
        ),
    ]
