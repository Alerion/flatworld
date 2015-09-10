# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models
import django.core.serializers.json
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0005_city_buildings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='buildings',
            field=utils.models.JSONField(null=True, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, schema=None, decode_kwargs={'parse_float': decimal.Decimal}, blank=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='stats',
            field=utils.models.JSONField(encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, schema=None, decode_kwargs={'parse_float': decimal.Decimal}),
        ),
        migrations.AlterField(
            model_name='world',
            name='params',
            field=utils.models.JSONField(encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, schema=None, decode_kwargs={'parse_float': decimal.Decimal}),
        ),
    ]
