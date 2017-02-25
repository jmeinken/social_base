# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-20 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('microfeed2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(verbose_name='start date')),
                ('start_time', models.TimeField(verbose_name='start time')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='end time')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='microfeed2.Post')),
            ],
            options={
                'ordering': ['start_date', 'start_time'],
            },
        ),
        migrations.RemoveField(
            model_name='eventpost',
            name='post',
        ),
        migrations.RemoveField(
            model_name='eventposttime',
            name='event_post',
        ),
        migrations.DeleteModel(
            name='EventPost',
        ),
        migrations.DeleteModel(
            name='EventPostTime',
        ),
    ]