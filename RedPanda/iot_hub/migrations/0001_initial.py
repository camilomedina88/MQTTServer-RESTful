# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('name', models.CharField(default='', max_length=50)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=250)),
                ('source_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('edition_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=250)),
                ('operand', models.CharField(choices=[('MT', 'More than'), ('LT', 'Less than'), ('EQ', 'Equal'), ('ME', 'More or equal than'), ('LE', 'Less or equal than')], default='EQ', max_length=2)),
                ('compare_value', models.FloatField()),
                ('action', models.CharField(choices=[('SMS', 'Send an SMS'), ('TEL', 'Send a telegram message'), ('EMA', 'Send an email'), ('SET', 'Set a variable')], default='SET', max_length=3)),
                ('value_set', models.FloatField()),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot_hub.DataSource')),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('name', models.CharField(default='', max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('icon', models.CharField(max_length=50)),
                ('var_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot_hub.DataSource')),
            ],
        ),
        migrations.CreateModel(
            name='VarValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('location', models.CharField(max_length=100)),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot_hub.Variable')),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('widget_type', models.CharField(choices=[('CHT', 'Chart'), ('MTC', 'Metric'), ('IND', 'Indicator'), ('BUTN', 'Button')], default='CHT', max_length=3)),
                ('datapoints', models.IntegerField()),
                ('data_variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot_hub.Variable')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='data_variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot_hub.Variable'),
        ),
        migrations.AddField(
            model_name='event',
            name='set_data_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_requests_created', to='iot_hub.DataSource'),
        ),
        migrations.AddField(
            model_name='event',
            name='set_data_variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_requests_created', to='iot_hub.Variable'),
        ),
    ]
