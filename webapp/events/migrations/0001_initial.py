# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import decimal
import django.core.serializers.json
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0007_auto_20150923_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined', models.DateTimeField()),
                ('outfit', utils.models.JSONField(schema=None, blank=True, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
                ('result_roll', models.PositiveIntegerField(blank=True, null=True)),
                ('loot', utils.models.JSONField(schema=None, blank=True, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
                ('city', models.ForeignKey(to='world.City')),
            ],
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField()),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('last_till', models.DateTimeField(blank=True, null=True)),
                ('repeatable', models.BooleanField(default=False)),
                ('required', models.BooleanField(default=False)),
                ('duration', models.IntegerField()),
                ('start_position', models.IntegerField(default=-100)),
                ('roll_width', models.IntegerField(default=100)),
                ('results', utils.models.JSONField(schema=None, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
                ('requirements', utils.models.JSONField(schema=None, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
                ('city', models.ManyToManyField(blank=True, to='world.City')),
                ('region', models.ManyToManyField(blank=True, to='world.Region')),
                ('world', models.ForeignKey(to='world.World')),
            ],
        ),
        migrations.AddField(
            model_name='participation',
            name='quest',
            field=models.ForeignKey(to='events.Quest'),
        ),
    ]
