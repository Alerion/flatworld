# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import postgres.fields
import decimal
import django.core.serializers.json


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_auto_20150825_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='world',
            name='points',
        ),
        migrations.RemoveField(
            model_name='world',
            name='seed',
        ),
        migrations.AlterField(
            model_name='world',
            name='params',
            field=postgres.fields.JSONField(decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}),
        ),
    ]
