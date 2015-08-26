"""
Keep these objects as simple as possible. They are passed via 0MQ with Pickle.
"""
from engine.base import Model
from engine import fields
# FIXME: WORLD_PARAMS is used in generate_world command. Not sure this is the best place,
# because requires to add the main folder to python paths.
DEFAULT_WORLD_PARAMS = {
    'start_population': 2000,
    'base_population_growth': 0.05,
    'points': None,
    'seed': None
}


class WorldParams(Model):
    start_population = fields.IntegerField()
    base_population_growth = fields.FloatField()
    points = fields.IntegerField()
    seed = fields.CharField()


class World(Model):
    id = fields.IntegerField()
    created = fields.DateTimeField()
    name = fields.CharField()
    params = fields.ModelField(WorldParams)

    def __init__(self, data):
        super().__init__(data)
        self.regions = {}

    def to_dict(self, serial=True):
        output = super().to_dict(serial)

        output['regions'] = {}
        for region_id, region in self.regions.items():
            output['regions'][region_id] = region.to_dict(serial)

        return output


class Region(Model):
    id = fields.IntegerField()
    geom = fields.GeoJSONField()
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


class CityStats(Model):
    population = fields.FloatField()
    population_growth = fields.FloatField()


class City(Model):
    id = fields.IntegerField()
    capital = fields.BooleanField()
    coords = fields.GeoJSONField()
    name = fields.CharField()
    stats = fields.ModelField(CityStats)
    region_id = fields.IntegerField()
    world_id = fields.IntegerField()

    def __init__(self, data, world, region):
        super().__init__(data)
        self.world = world
        self.region = region
