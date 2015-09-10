from .base import Model
from . import fields


properties_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'title': 'Building properties',
    'type': 'object',
    'properties': {
        'tax': {
            'description': 'How much every citizen pays per day.',
            'type': 'number',
            'minimum': 0,
            'exclusiveMinimum': True
        },
        'population_growth': {
            'description': 'Population growth in percent per day.',
            'type': 'number',
            'minimum': 0,
            'exclusiveMinimum': True,
            'maximum': 1
        },
        'pasive_income': {
            'description': 'Flat income per day.',
            'type': 'number'
        }
    }
}


class Building(Model):
    id = fields.IntegerField()
    name = fields.CharField()
    description = fields.CharField()
    build_time = fields.IntegerField()
    cost_money = fields.IntegerField()
    cost_population = fields.IntegerField()
    properties = fields.JSONField()
    properties_description = fields.JSONField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.properties_description = {}
        for key in self.properties.keys():
            self.properties_description[key] = properties_schema['properties'][key]['description']
