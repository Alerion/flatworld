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
        },
        'iron_income': {
            'description': 'Iron income per day.',
            'type': 'number'
        },
        'stone_income': {
            'description': 'Stone income per day.',
            'type': 'number'
        },
        'wood_income': {
            'description': 'Wood income per day.',
            'type': 'number'
        }
    }
}


class BuildingTier(Model):
    id = fields.IntegerField()
    level = fields.IntegerField()
    build_time = fields.IntegerField()
    cost_money = fields.IntegerField()
    cost_population = fields.IntegerField()
    cost_iron = fields.IntegerField()
    cost_stone = fields.IntegerField()
    cost_wood = fields.IntegerField()
    properties = fields.JSONField()
    properties_description = fields.JSONField()

    def set_data(self, data):
        super().set_data(data)
        self.properties_description = {}
        for key in self.properties.keys():
            self.properties_description[key] = properties_schema['properties'][key]['description']


class Building(Model):
    id = fields.IntegerField()
    name = fields.CharField()
    description = fields.CharField()
    tiers = fields.ModelDictCollectionField(BuildingTier)
