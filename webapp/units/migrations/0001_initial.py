# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models
import django.core.serializers.json
import decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('properties', utils.models.JSONField(schema=None, decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder})),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('attack', models.PositiveIntegerField()),
                ('defence', models.PositiveIntegerField()),
                ('properties', utils.models.JSONField(schema=None, decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder})),
                ('train_time', models.IntegerField(help_text='in seconds for default speed')),
                ('cost_money', models.IntegerField()),
                ('cost_population', models.IntegerField(default=1)),
                ('cost_iron', models.IntegerField()),
                ('cost_stone', models.IntegerField()),
                ('cost_wood', models.IntegerField()),
                ('parent', models.ForeignKey(to='units.Unit', null=True, blank=True)),
                ('type', models.ForeignKey(to='units.Type')),
            ],
        ),
    ]
