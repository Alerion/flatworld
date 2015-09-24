# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models
import django.core.serializers.json
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='finished',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='quest',
            name='requirements',
            field=utils.models.JSONField(schema=None, decode_kwargs={'parse_float': decimal.Decimal}, blank=True, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}),
        ),
    ]
