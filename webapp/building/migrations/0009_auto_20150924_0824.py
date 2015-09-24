# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.validators
import django.core.serializers.json
import utils.models
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0008_auto_20150921_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingtier',
            name='properties',
            field=utils.models.JSONField(schema={'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'minimum': 0, 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'tax': {'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.', 'minimum': 0}}, 'type': 'object', 'title': 'Building properties'}, validators=[utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'minimum': 0, 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'tax': {'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.', 'minimum': 0}}, 'type': 'object', 'title': 'Building properties'}), utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'minimum': 0, 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'tax': {'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.', 'minimum': 0}}, 'type': 'object', 'title': 'Building properties'}), utils.validators.JsonSchemaValidator({'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'minimum': 0, 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'tax': {'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.', 'minimum': 0}}, 'type': 'object', 'title': 'Building properties'})], encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal}),
        ),
    ]
