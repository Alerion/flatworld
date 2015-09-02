# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.serializers.json
import postgres.fields
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0004_auto_20150902_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='buildings',
            field=postgres.fields.JSONField(decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, null=True, blank=True),
        ),
    ]
