# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.validators
import django.core.serializers.json
import utils.models
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0004_auto_20150910_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='properties',
            field=utils.models.JSONField(encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, validators=[utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'population_growth': {'exclusiveMinimum': True, 'description': 'Population growth percent per day.', 'minimum': 0, 'maximum': 1, 'type': 'number'}, 'tax': {'exclusiveMinimum': True, 'description': 'How many every citizen pays per day.', 'minimum': 0, 'type': 'number'}}, 'type': 'object', 'title': 'Building properties'}), utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'population_growth': {'exclusiveMinimum': True, 'description': 'Population growth percent per day.', 'minimum': 0, 'maximum': 1, 'type': 'number'}, 'tax': {'exclusiveMinimum': True, 'description': 'How many every citizen pays per day.', 'minimum': 0, 'type': 'number'}}, 'type': 'object', 'title': 'Building properties'}), utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'population_growth': {'exclusiveMinimum': True, 'description': 'Population growth percent per day.', 'minimum': 0, 'maximum': 1, 'type': 'number'}, 'tax': {'exclusiveMinimum': True, 'description': 'How many every citizen pays per day.', 'minimum': 0, 'type': 'number'}}, 'type': 'object', 'title': 'Building properties'})], schema={'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'population_growth': {'exclusiveMinimum': True, 'description': 'Population growth percent per day.', 'minimum': 0, 'maximum': 1, 'type': 'number'}, 'tax': {'exclusiveMinimum': True, 'description': 'How many every citizen pays per day.', 'minimum': 0, 'type': 'number'}}, 'type': 'object', 'title': 'Building properties'}, decode_kwargs={'parse_float': decimal.Decimal}),
        ),
    ]
