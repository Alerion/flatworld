# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import decimal
import django.core.serializers.json
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0006_auto_20150910_0812'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cities'},
        ),
        migrations.AddField(
            model_name='city',
            name='units',
            field=utils.models.JSONField(blank=True, decode_kwargs={'parse_float': decimal.Decimal}, null=True, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, schema=None),
        ),
    ]
