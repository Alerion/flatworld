import asyncio

from .exceptions import CityDoesNotExist, BuildingDoesNotExist


class WorldEngine:

    def __init__(self, loop, events, world):
        self.world = world
        self._events = events
        self._loop = loop
        self.speed = world.params.speed
        self.layers = [
            MoneyLayer(world),
            PopulationLayer(world),
            BuildLayer(world)
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

    def build(self, city_id, building_id):
        city = self.world.cities.get(city_id)
        if not city:
            raise CityDoesNotExist(city_id)

        building = self.world.buildings.get(building_id)
        if not building:
            raise BuildingDoesNotExist(building_id)

        city.build(building)
        return city

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
