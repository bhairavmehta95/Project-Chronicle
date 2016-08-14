# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speech', '0011_auto_20160813_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
