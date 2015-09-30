from random import random
from datetime import datetime, timezone

from . import fields
from .base import Model
from ..exceptions import BuildError, QuestError


class ActiveQuest(Model):
    id = fields.IntegerField()
    quest_id = fields.IntegerField()
    joined = fields.DateTimeField()
    finished = fields.DateTimeField()
    closed = fields.DateTimeField()
    outfit = fields.JSONField()
    result_roll = fields.FloatField()
    loot = fields.JSONField()
    progress = fields.IntegerField()

    def finish(self):
        self.finished = datetime.now(timezone.utc)
        self.result_roll = random() * 100
        self.loot = {}
        self.progress = 0

    def close(self):
        self.closed = datetime.now(timezone.utc)

    @classmethod
    def start(cls, quest):
        return cls({
            'quest_id': quest.id,
            'joined': datetime.now(timezone.utc),
            'outfit': {},
            'progress': quest.duration,
            'finished': None,
            'closed': None,
            'result_roll': None,
            'loot': None
        })


class CityBuilding(Model):
    level = fields.IntegerField()
    in_progress = fields.BooleanField()
    build_progress = fields.IntegerField()
    building_id = fields.IntegerField()

    @property
    def building(self):
        return self.city.world.buildings[self.building_id]

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


class CityUnit(Model):
    number = fields.IntegerField()
    queue = fields.IntegerField()
    unit_id = fields.IntegerField()

    @property
    def unit(self):
        return self.city.world.units[self.unit_id]


class CityStats(Model):
    population = fields.FloatField()
    money = fields.FloatField()

    population_growth = fields.FloatField(improvable=True)
    pasive_income = fields.FloatField(improvable=True)
    tax = fields.FloatField(improvable=True)

    iron = fields.FloatField()
    iron_income = fields.FloatField(improvable=True)
    stone = fields.FloatField()
    stone_income = fields.FloatField(improvable=True)
    wood = fields.FloatField()
    wood_income = fields.FloatField(improvable=True)

    def apply_buildings(self, city_buildings):
        # Reset improvable fields with default
        self.reset()

        for city_building in city_buildings.values():
            for building_tier in city_building.tiers:
                properties = building_tier.properties
                for key, delta in properties.items():
                    current_value = getattr(self, key)
                    new_value = current_value + delta
                    setattr(self, key, new_value)


class City(Model):
    id = fields.IntegerField()
    active_quests = fields.ModelDictCollectionField(ActiveQuest, related_name='city')
    buildings = fields.ModelDictCollectionField(CityBuilding, related_name='city')
    capital = fields.BooleanField()
    coords = fields.JSONField()
    name = fields.CharField()
    region_id = fields.IntegerField()
    stats = fields.ModelField(CityStats)
    units = fields.ModelDictCollectionField(CityUnit, related_name='city')
    user_id = fields.IntegerField()
    world_id = fields.IntegerField()

    def __init__(self, data, world, region):
        super().__init__(data)
        self.world = world
        self.region = region
        self._apply_buildings()

    def _apply_buildings(self):
        self.stats.apply_buildings(self.buildings)

    def update_population(self, delta):
        self.stats.population += self.stats.population_growth * delta

    def update_money(self, delta):
        stats = self.stats
        stats.money += (stats.pasive_income + stats.population * stats.tax) * delta

    def update_iron(self, delta):
        self.stats.iron += self.stats.iron_income * delta

    def update_stone(self, delta):
        self.stats.stone += self.stats.stone_income * delta

    def update_wood(self, delta):
        self.stats.wood += self.stats.wood_income * delta

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

        if building_tier.cost_iron > self.stats.iron:
            raise BuildError(self.id, building.id, 'Not enough iron.')

        if building_tier.cost_stone > self.stats.stone:
            raise BuildError(self.id, building.id, 'Not enough stone.')

        if building_tier.cost_wood > self.stats.wood:
            raise BuildError(self.id, building.id, 'Not enough wood.')

        self.stats.money -= building_tier.cost_money
        self.stats.population -= building_tier.cost_population
        self.stats.iron -= building_tier.cost_iron
        self.stats.stone -= building_tier.cost_stone
        self.stats.wood -= building_tier.cost_wood

        city_building.start_build(building_tier)

    def start_quest(self, quest):
        # Check here that quest is not started and that city has enough resources.
        # Does not check availability.
        active_quest = self.active_quests.get(quest.id)

        if active_quest and not active_quest.closed:
            raise QuestError(self.id, quest.id, 'Quest already in progress.')

        self.active_quests[quest.id] = ActiveQuest.start(quest)

    def close_quest(self, quest):
        active_quest = self.active_quests.get(quest.id)

        if not active_quest or not active_quest.finished:
            raise QuestError(self.id, quest.id, 'Quest is not finished.')

        if active_quest.closed:
            raise QuestError(self.id, quest.id, 'Quest already closed.')

        active_quest.close()
        self.active_quests.pop(quest.id)

    def update_quests(self, delta):
        quest_finished = False

        for active_quest in self.active_quests.values():
            if not active_quest.finished:
                active_quest.progress -= delta
                if active_quest.progress <= 0:
                    active_quest.finish()
                    quest_finished = True

        return quest_finished

    def to_dict(self, detailed=False, **kwargs):
        # detailed is for future to dump user city and other cities
        return super().to_dict(**kwargs)
