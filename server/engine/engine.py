import asyncio


class WorldEngine:

    def __init__(self, events, world):
        self.world = world
        self._events = events
        self.speed = world.params.speed

    def run(self, elapsed):
        # All "growths" are per day
        delta = (elapsed * self.speed) / (3600 * 24)
        for city in self.world.cities():
            city.stats.population *= (1 + city.stats.population_growth * delta)

        # self._publish('updates').update_cities(self.cities)

    def get_world(self):
        return self.world

    def _publish(self, topic):
        return self._events.publish('{}:{}'.format(topic, self.world_id))
