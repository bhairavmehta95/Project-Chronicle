# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speech', '0010_auto_20160813_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testing',
            name='question_text',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
