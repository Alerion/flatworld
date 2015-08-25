# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.serializers.json
import postgres.fields
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='stats',
            field=postgres.fields.JSONField(default={}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='world',
            name='params',
            field=postgres.fields.JSONField(default={'start_population': 2000, 'base_population_growth': 0.05}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal}),
        ),
    ]
