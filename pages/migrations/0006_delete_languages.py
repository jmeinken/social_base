# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 03:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_languages'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Languages',
        ),
    ]
