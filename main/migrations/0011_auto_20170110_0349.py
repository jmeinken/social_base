# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20170110_0343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='id',
        ),
        migrations.AddField(
            model_name='language',
            name='code',
            field=models.CharField(default='en', max_length=6, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
