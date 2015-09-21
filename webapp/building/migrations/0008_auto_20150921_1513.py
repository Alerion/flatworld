# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.validators
import django.core.serializers.json
import decimal
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0007_auto_20150914_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingtier',
            name='cost_iron',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildingtier',
            name='cost_stone',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildingtier',
            name='cost_wood',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buildingtier',
            name='properties',
            field=utils.models.JSONField(validators=[utils.validators.JsonSchemaValidator({'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'type': 'object', 'properties': {'population_growth': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'tax': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}}}), utils.validators.JsonSchemaValidator({'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'type': 'object', 'properties': {'population_growth': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'tax': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}}}), utils.validators.JsonSchemaValidator({'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'type': 'object', 'properties': {'population_growth': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'tax': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}}})], encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal}, schema={'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'type': 'object', 'properties': {'population_growth': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'Population growth in percent per day.', 'maximum': 1}, 'wood_income': {'type': 'number', 'description': 'Wood income per day.'}, 'pasive_income': {'type': 'number', 'description': 'Flat income per day.'}, 'tax': {'minimum': 0, 'exclusiveMinimum': True, 'type': 'number', 'description': 'How much every citizen pays per day.'}, 'stone_income': {'type': 'number', 'description': 'Stone income per day.'}, 'iron_income': {'type': 'number', 'description': 'Iron income per day.'}}}),
        ),
    ]
