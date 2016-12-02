# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file_base_name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='app_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='model_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
