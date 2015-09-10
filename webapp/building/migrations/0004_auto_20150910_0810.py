# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import decimal
import utils.validators
import django.core.serializers.json
import postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0003_auto_20150903_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='properties',
            field=postgres.fields.JSONField(validators=[utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'type': 'object', 'properties': {'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'tax': {'description': 'How many every citizen pays per day.', 'minimum': 0, 'type': 'number', 'exclusiveMinimum': True}, 'population_growth': {'description': 'Population growth percent per day.', 'minimum': 0, 'type': 'number', 'exclusiveMinimum': True, 'maximum': 1}}, 'title': 'Building properties'})], encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal}),
        ),
    ]
