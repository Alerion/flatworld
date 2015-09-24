# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models
import django.core.serializers.json
import decimal
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0009_auto_20150924_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingtier',
            name='properties',
            field=utils.models.JSONField(schema={'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'iron_income': {'description': 'Iron income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}, 'stone_income': {'description': 'Stone income per day.', 'type': 'number'}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'wood_income': {'description': 'Wood income per day.', 'type': 'number'}, 'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'maximum': 1, 'minimum': 0}}}, decode_kwargs={'parse_float': decimal.Decimal}, validators=[utils.validators.JsonSchemaValidator({'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'iron_income': {'description': 'Iron income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}, 'stone_income': {'description': 'Stone income per day.', 'type': 'number'}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'wood_income': {'description': 'Wood income per day.', 'type': 'number'}, 'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'maximum': 1, 'minimum': 0}}}), utils.validators.JsonSchemaValidator({'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'iron_income': {'description': 'Iron income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}, 'stone_income': {'description': 'Stone income per day.', 'type': 'number'}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'wood_income': {'description': 'Wood income per day.', 'type': 'number'}, 'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'maximum': 1, 'minimum': 0}}}), utils.validators.JsonSchemaValidator({'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'iron_income': {'description': 'Iron income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}, 'stone_income': {'description': 'Stone income per day.', 'type': 'number'}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'wood_income': {'description': 'Wood income per day.', 'type': 'number'}, 'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'maximum': 1, 'minimum': 0}}})], encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}),
        ),
    ]
