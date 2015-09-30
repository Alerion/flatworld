import asyncio
from datetime import datetime, timezone

from .exceptions import CityDoesNotExist, BuildingDoesNotExist, QuestDoesNotExist
from .models.base import ModelsDict


class WorldEngine:

    def __init__(self, loop, events, world):
        self.world = world
        self._events = events
        self._loop = loop
        self.speed = world.params.speed
        self.layers = [
            MoneyLayer(world),
            PopulationLayer(world),
            IronLayer(world),
            StoneLayer(world),
            WoodLayer(world),
            BuildLayer(world),
            QuestsLayer(world),
        ]

    @asyncio.coroutine
    def run(self, elapsed):
        """
        All "growths" are per real day if `speed` is 1.
        So one real day is one unit of game time. And you can use `speed` to change
        game speed time.
        """
        delta = (elapsed * self.speed) / (3600 * 24)
        notify = False

        for layer in self.layers:
            if layer.run(delta, elapsed) and not notify:
                notify = True

        if notify:
            self._loop.call_soon(self._update_world)

    def get_world(self):
        return self.world

    def get_city(self, city_id):
        city = self.world.cities.get(city_id)
        if not city:
            raise CityDoesNotExist(city_id)
        return city

    def get_building(self, building_id):
        building = self.world.buildings.get(building_id)
        if not building:
            raise BuildingDoesNotExist(building_id)
        return building

    def build(self, city_id, building_id):
        city = self.get_city(city_id)
        city.build(self.get_building(building_id))
        return city

    def get_quests(self, city_id):
        city = self.get_city(city_id)
        quests = ModelsDict()

        for quest_id, quest in self.world.quests.items():
            if (not quest.cities and not quest.regions) or \
                    city.id in quest.cities or city.region_id in quest.regions:
                # FIXME: Filter out completed and not repeatable quests
                quests[quest_id] = quest

        return quests

    def get_quest(self, quest_id):
        quest = self.world.quests.get(quest_id)
        if not quest:
            raise QuestDoesNotExist(quest_id)
        return quest

    def get_quest_for_city(self, city_id, quest_id):
        quests = self.get_quests(city_id)
        quest = quests.get(quest_id)
        if not quest:
            raise QuestDoesNotExist(quest_id, city_id)
        return quest

    def start_quest(self, city_id, quest_id):
        """
        Check here that quest is available for city.
        """
        city = self.get_city(city_id)
        quest = self.get_quest_for_city(city_id, quest_id)

        if quest.finished or (quest.last_till and datetime.now(timezone.utc) >= quest.last_till):
            raise QuestDoesNotExist(quest_id, city_id)

        city.start_quest(quest)
        return city

    def close_quest(self, city_id, quest_id):
        """
        Check here that quest is available for city.
        """
        city = self.get_city(city_id)
        quest = self.get_quest_for_city(city_id, quest_id)
        city.close_quest(quest)
        self._check_closed_quest(quest, city)
        return city

    def _check_closed_quest(self, quest, city):
        """
        Check if we can cleanup closed quest.
        """
        # FIXME: Save cleaned quests to DB
        # User can repeat quest, just clean active_quest
        if quest.repeatable:
            city.cleanup_active_quest(quest)
            return

        # Quest exists only for this city, we can cleanup this quest
        if quest.is_private_for_city(city):
            quest.finish()
            city.cleanup_active_quest(quest)
            self.world.cleanup_quest(quest)
            self._loop.call_soon(self._update_quests, city)
            return

    def _update_quests(self, city):
        quests = self.get_quests(city.id)
        return self._events.publish('updates:city:{}'.format(city.id)) \
            .update_quests(quests)

    def _update_world(self):
        return self._events.publish('updates:world:{}'.format(self.world.id)) \
            .update_world(self.world)


class SimulationLayer:
    notify_treshhold = 0  # seconds

    def __init__(self, world):
        self.world = world
        self._from_last_notify = 0

    def run(self, delta, elapsed):
        """
        `delta` - game time from last run. In unit of game time.
        `elapsed` - real time from last run. Used to check notification or how often do updates,
        so should not be affected with game speed parameter.

        Update world. Return `True` if it updates should be sent to client. If nothing happens,
        always return `False`. Call `_check_notify` to update `_from_last_notify`.
        """
        pass

    def _check_notify(self, elapsed):
        """
        Return `True` if engine should send updates to client. Used to prevent spam for
        often updated parameters.

        Uses `notify_treshhold`.

        If it is equals `None`, never notify. Can be used for internal parameters that never
        seed by client.

        If it is equal `0`, send notification every time `run` do some updated.

        It is is equal some `N`, send updates every `N` seconds.
        """
        if self.notify_treshhold is None:
            return False

        if self.notify_treshhold == 0:
            return True

        self._from_last_notify += elapsed

        if self._from_last_notify > self.notify_treshhold:
            self._from_last_notify = 0
            return True

        return False


class PopulationLayer(SimulationLayer):
    notify_treshhold = 15

    def run(self, delta, elapsed):
        for city in self.world.cities.values():
            city.update_population(delta)

        return self._check_notify(elapsed)


class MoneyLayer(SimulationLayer):
    notify_treshhold = 15

    def run(self, delta, elapsed):
        for city in self.world.cities.values():
            city.update_money(delta)

        return self._check_notify(elapsed)


class IronLayer(SimulationLayer):
    notify_treshhold = 15

    def run(self, delta, elapsed):
        for city in self.world.cities.values():
            city.update_iron(delta)

        return self._check_notify(elapsed)


class StoneLayer(SimulationLayer):
    notify_treshhold = 15

    def run(self, delta, elapsed):
        for city in self.world.cities.values():
            city.update_stone(delta)

        return self._check_notify(elapsed)


class WoodLayer(SimulationLayer):
    notify_treshhold = 15

    def run(self, delta, elapsed):
        for city in self.world.cities.values():
            city.update_wood(delta)

        return self._check_notify(elapsed)


class BuildLayer(SimulationLayer):
    notify_treshhold = None

    def run(self, delta, elapsed):
        notify = []
        # FIXME: Check just buildings in progress
        for city in self.world.cities.values():
            build_finished = city.update_build(delta)
            if build_finished:
                notify.append(city.id)

        return bool(notify)


class QuestsLayer(SimulationLayer):
    notify_treshhold = None

    def run(self, delta, elapsed):
        notify = []

        for city in self.world.cities.values():
            quest_finished = city.update_quests(delta)
            if quest_finished:
                notify.append(city.id)

        return bool(notify)
