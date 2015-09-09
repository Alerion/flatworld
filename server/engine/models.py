"""
Keep these objects as simple as possible. They are passed via 0MQ with Pickle.
"""
from . import fields
from .base import Model
from .exceptions import BuildError
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


class Building(Model):
    id = fields.IntegerField()
    name = fields.CharField()
    description = fields.CharField()
    build_time = fields.IntegerField()
    cost_money = fields.IntegerField()
    cost_population = fields.IntegerField()
    properties = fields.JSONField()


class CityBuilding(Model):
    level = fields.IntegerField()
    in_progress = fields.BooleanField()
    build_progress = fields.IntegerField()
    building_id = fields.IntegerField()

    def __init__(self, data):
        super().__init__(data)
        self.building = None

    def start_build(self):
        self.in_progress = True
        self.build_progress = self.building.build_time

    def finish_build(self):
        self.in_progress = False
        self.build_progress = 0
        self.level += 1


class CityStats(Model):
    population = fields.FloatField()
    population_growth = fields.FloatField()
    money = fields.FloatField()
    pasive_income = fields.FloatField()
    tax = fields.FloatField()


class City(Model):
    id = fields.IntegerField()
    capital = fields.BooleanField()
    coords = fields.JSONField()
    buildings = fields.ModelDictCollectionField(CityBuilding)
    name = fields.CharField()
    stats = fields.ModelField(CityStats)
    region_id = fields.IntegerField()
    world_id = fields.IntegerField()
    user_id = fields.IntegerField()

    def __init__(self, data, world, region):
        super().__init__(data)
        self.world = world
        self.region = region
        self._init_city_building()

    def update_population(self, delta):
        self.stats.population *= (1 + self.stats.population_growth * delta)

    def update_money(self, delta):
        stats = self.stats
        stats.money += (stats.pasive_income + stats.population * stats.tax) * delta

    def update_build(self, delta):
        build_finished = False

        for city_building in self.buildings.values():
            if city_building.in_progress:
                city_building.build_progress -= delta
                if city_building.build_progress <= 0:
                    city_building.finish_build()
                    build_finished = True

        return build_finished

    def _init_city_building(self):
        for building_id, building in self.world.buildings.items():
            if building_id not in self.buildings:
                city_building = CityBuilding({
                    'level': 0,
                    'in_progress': False,
                    'building_id': building_id,
                    'build_progress': 0
                })
                self.buildings[building_id] = city_building

            self.buildings[building_id].building = building

    def build(self, building):
        city_building = self.buildings[building.id]

        if city_building.in_progress:
            raise BuildError(self.id, building.id, 'Building already in progress.')

        if building.cost_money > self.stats.money:
            raise BuildError(self.id, building.id, 'Not enough money.')

        if building.cost_population > self.stats.population:
            raise BuildError(self.id, building.id, 'Not enough population.')

        self.stats.money -= building.cost_money
        self.stats.population -= building.cost_population

        # TODO: Add resources check and consume
        city_building.start_build()

    def to_dict(self, detailed=False, serial=True):
        return super().to_dict(serial=serial)
