# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 03:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('iot_hub', '0002_auto_20161114_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(default=django.utils.timezone.now, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='description',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='variable',
            name='description',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='variable',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
