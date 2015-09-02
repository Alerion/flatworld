# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import postgres.fields
import django.core.serializers.json
import decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('build_time', models.IntegerField(help_text='in seconds')),
                ('cost_money', models.IntegerField()),
                ('cost_population', models.IntegerField()),
                ('properties', postgres.fields.JSONField(encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal})),
            ],
        ),
    ]
