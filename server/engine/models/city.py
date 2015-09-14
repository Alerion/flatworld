import ujson

from . import fields
from .base import Model
from ..exceptions import BuildError


class CityBuilding(Model):
    level = fields.IntegerField()
    in_progress = fields.BooleanField()
    build_progress = fields.IntegerField()
    building_id = fields.IntegerField()

    def __init__(self, data):
        super().__init__(data)
        self.building = None

    def set_building(self, building):
        self.building = building

    @property
    def tiers(self):
        for index in range(0, self.level):
            yield self.building.tiers[index + 1]

    def start_build(self, building_tier):
        assert building_tier.level == self.level + 1
        self.in_progress = True
        self.build_progress = building_tier.build_time

    def finish_build(self):
        self.in_progress = False
        self.build_progress = 0
        self.level += 1


class CityStats(Model):
    population = fields.FloatField()
    money = fields.FloatField()

    population_growth = fields.FloatField(improvable=True)
    pasive_income = fields.FloatField(improvable=True)
    tax = fields.FloatField(improvable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_data = None

    def set_data(self, data, is_json=False):
        if is_json:
            data = ujson.loads(data)

        self._initial_data = {}

        for name, field in self._clsfields.items():
            if field.improvable:
                self._initial_data[name] = data[name]

        super().set_data(data)

    def apply_buildings(self, city_buildings):
        # Reset improvable fields with default
        self.set_data(self._initial_data)

        for city_building in city_buildings.values():
            for building_tier in city_building.tiers:
                properties = building_tier.properties
                for key, delta in properties.items():
                    current_value = getattr(self, key)
                    new_value = current_value + delta
                    setattr(self, key, new_value)


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
        self._apply_buildings()

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
            # FIXME: Weird initialization
            self.buildings[building_id].set_building(building)

    def _apply_buildings(self):
        self.stats.apply_buildings(self.buildings)

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

        if build_finished:
            self._apply_buildings()

        return build_finished

    def build(self, building):
        city_building = self.buildings[building.id]

        if city_building.in_progress:
            raise BuildError(self.id, building.id, 'Building already in progress.')

        try:
            building_tier = building.tiers[city_building.level + 1]
        except KeyError:
            raise BuildError(self.id, building.id, 'Building already has max level.')

        if building_tier.cost_money > self.stats.money:
            raise BuildError(self.id, building.id, 'Not enough money.')

        if building_tier.cost_population > self.stats.population:
            raise BuildError(self.id, building.id, 'Not enough population.')

        self.stats.money -= building_tier.cost_money
        self.stats.population -= building_tier.cost_population

        # TODO: Add resources check and consume
        city_building.start_build(building_tier)

    def to_dict(self, detailed=False, serial=True):
        return super().to_dict(serial=serial)
