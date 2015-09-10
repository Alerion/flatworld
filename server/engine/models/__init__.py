"""
Keep these objects as simple as possible. They are passed via 0MQ with Pickle.
"""
from . import fields
from .base import Model

from .building import Building
from .city import City

__all__ = ['DEFAULT_WORLD_PARAMS', 'Building', 'World', 'Region', 'City']

# FIXME: WORLD_PARAMS is used in generate_world command. Not sure this is the best place,
# because requires to add the main folder to python paths.
DEFAULT_WORLD_PARAMS = {
    # Population
    'start_population': 2000,
    'base_population_growth': 0.05,
    # Money
    'start_money': 500,
    'base_income': 50,
    'base_tax': 0.1,
    # General
    'points': None,
    'seed': None,
    'speed': 1.
}


class WorldParams(Model):
    start_population = fields.IntegerField()
    base_population_growth = fields.FloatField()
    start_money = fields.IntegerField()
    base_income = fields.IntegerField()
    points = fields.IntegerField()
    seed = fields.CharField()
    speed = fields.FloatField()


class World(Model):
    id = fields.IntegerField()
    created = fields.DateTimeField()
    name = fields.CharField()
    params = fields.ModelField(WorldParams)

    def __init__(self, data):
        super().__init__(data)
        self.regions = {}
        self.cities = {}
        self.buildings = {}

    def to_dict(self, serial=True):
        output = super().to_dict(serial)

        output['regions'] = {}
        for region_id, region in self.regions.items():
            output['regions'][region_id] = region.to_dict(serial)

        # FIXME: Do not send full information about every city
        return output


class Region(Model):
    id = fields.IntegerField()
    geom = fields.JSONField()
    name = fields.CharField()
    world_id = fields.IntegerField()

    def __init__(self, data, world):
        super().__init__(data)
        self.world = world
        self.neighbors = {}
        self.cities = {}

    def to_dict(self, serial=True):
        output = super().to_dict(serial)

        output['cities'] = {}
        for city_id, city in self.cities.items():
            output['cities'][city_id] = city.to_dict(serial)

        output['neighbors'] = []
        for neighbor_id in self.neighbors.keys():
            output['neighbors'].append(neighbor_id)

        return output
