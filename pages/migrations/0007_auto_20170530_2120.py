# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-30 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20170529_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='contact_email',
            field=models.CharField(blank=True, max_length=240, null=True, verbose_name='contact email'),
        ),
        migrations.AlterField(
            model_name='page',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='address'),
        ),
    ]
