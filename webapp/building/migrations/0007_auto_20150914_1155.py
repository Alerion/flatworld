# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models
import decimal
import utils.validators
import django.core.serializers.json


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0006_delete_building'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BuildingTier',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField(default=1)),
                ('build_time', models.IntegerField(help_text='in seconds for default speed')),
                ('cost_money', models.IntegerField()),
                ('cost_population', models.IntegerField()),
                ('properties', utils.models.JSONField(schema={'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0, 'maximum': 1}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}}}, validators=[utils.validators.JsonSchemaValidator({'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0, 'maximum': 1}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}}}), utils.validators.JsonSchemaValidator({'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0, 'maximum': 1}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}}}), utils.validators.JsonSchemaValidator({'type': 'object', 'title': 'Building properties', '$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'population_growth': {'description': 'Population growth in percent per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0, 'maximum': 1}, 'pasive_income': {'description': 'Flat income per day.', 'type': 'number'}, 'tax': {'description': 'How much every citizen pays per day.', 'type': 'number', 'exclusiveMinimum': True, 'minimum': 0}}})], decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder})),
                ('building', models.ForeignKey(to='building.Building')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='buildingtier',
            unique_together=set([('building', 'level')]),
        ),
    ]
