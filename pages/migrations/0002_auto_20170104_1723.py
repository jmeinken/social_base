# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-04 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='add_microfeed',
        ),
        migrations.RemoveField(
            model_name='pagecategory',
            name='add_microfeed',
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_set', to='pages.PageCategory'),
        ),
    ]