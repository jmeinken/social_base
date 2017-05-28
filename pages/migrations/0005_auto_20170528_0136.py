# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-28 01:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0004_auto_20170112_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('data', models.TextField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Page')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='pageaddress',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pageimage',
            name='page',
        ),
        migrations.AlterModelOptions(
            name='pagecategory',
            options={'ordering': ['order', 'title']},
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='order',
            field=models.IntegerField(default=0, verbose_name='order'),
        ),
        migrations.DeleteModel(
            name='PageAddress',
        ),
        migrations.DeleteModel(
            name='PageImage',
        ),
    ]
