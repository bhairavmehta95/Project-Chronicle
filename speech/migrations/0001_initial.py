# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_id', models.AutoField(serialize=False, primary_key=True)),
                ('class_name', models.CharField(max_length=100)),
                ('num_enrollments', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Completion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enrollments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_id', models.ForeignKey(to='speech.Class')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('question_subject', models.CharField(default=b'QUESTION', max_length=100)),
                ('question_text', models.TextField()),
                ('num_attempts', models.IntegerField(default=0)),
                ('num_accepted', models.IntegerField(default=0)),
                ('is_user_generated', models.BooleanField(default=False)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('percent_to_pass', models.FloatField(default=0.5)),
                ('class_id', models.ForeignKey(to='speech.Class')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SelfStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('f_name', models.CharField(max_length=30)),
                ('l_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Testing',
            fields=[
                ('test_id', models.AutoField(serialize=False, primary_key=True)),
                ('topic_name', models.CharField(max_length=100)),
                ('question_subject', models.CharField(max_length=100)),
                ('question_text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('topic_id', models.AutoField(serialize=False, primary_key=True)),
                ('topic_name', models.CharField(max_length=100)),
                ('num_questions', models.IntegerField(default=0)),
                ('class_id', models.ForeignKey(to='speech.Class')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='topic_id',
            field=models.ForeignKey(to='speech.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollments',
            name='student_id',
            field=models.ForeignKey(to='speech.Student'),
            preserve_default=True,
        ),
    ]
