import asyncio


class WorldEngine:

    def __init__(self, db, events, world_id):
        self.world_id = world_id
        self.world = None
        self._db = db
        self._events = events

    @asyncio.coroutine
    def init(self):
        self.world = yield from self._db.call.get_world(self.world_id)

    def run(self):
        for city in self.world.cities.values():
            city.stats.population *= 1 + city.stats.population_growth

        # self._publish('updates').update_cities(self.cities)

    def _publish(self, topic):
        return self._events.publish('{}:{}'.format(topic, self.world_id))

    def get_city_stats(self, city_id):
        return self.world.cities[city_id]

    def get_world(self):
        return self.world
