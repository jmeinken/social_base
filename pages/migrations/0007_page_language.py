# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 03:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20170110_0349'),
        ('pages', '0006_delete_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='language',
            field=models.ForeignKey(default='en', on_delete=django.db.models.deletion.PROTECT, to='main.Language'),
            preserve_default=False,
        ),
    ]
