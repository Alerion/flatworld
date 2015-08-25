import asyncio
import aiozmq.rpc
import os
from zmqrpc.translation_table import translation_table


class World:

    def __init__(self, db, events, world_id):
        self.world_id = world_id
        self.world = None
        self.cities = {}
        self.regions = {}
        self._db = db
        self._events = events

    @asyncio.coroutine
    def init(self):
        self.world = yield from self._db.call.get_world(self.world_id)

        for region in self.world['regions']:
            self.regions[region['id']] = region

            for city in region['cities']:
                self.cities[city['id']] = city

    def run(self):
        for region in self.world['regions']:
            for city in region['cities']:
                city['stats']['population'] *= 1 + city['stats']['population_growth']

        self.publish('updates').update_cities(self.cities)

    def publish(self, topic):
        return self._events.publish('{}:{}'.format(topic, self.world_id))

    def get_city_stats(self, city_id):
        return self.cities[city_id]


class ServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self, db, events, worlds):
        super().__init__()
        self.worlds = worlds
        self._db = db
        self._events = events

    @asyncio.coroutine
    def run(self):
        # self._events = yield from aiozmq.rpc.connect_pubsub(
        #     connect=os.environ['PROXY_PORT_5100_TCP'])
        # self._db = yield from aiozmq.rpc.connect_rpc(
        #     connect=os.environ['DBSERVER_PORT_5000_TCP'],
        #     translation_table=translation_table,
        #     timeout=5)

        while True:
            for world in self.worlds.values():
                world.run()

            yield from asyncio.sleep(30)

            # self.value += 1
            # print(self.value)
            # self._events.publish('updates:{}'.format(self.world_id)).set_value(self.value)

    @aiozmq.rpc.method
    def get_city_stats(self, world_id: int, city_id: int):
        return self.worlds[world_id].get_city_stats(city_id)


def main():
    loop = asyncio.get_event_loop()

    events = loop.run_until_complete(
        aiozmq.rpc.connect_pubsub(connect=os.environ['PROXY_PORT_5100_TCP']))

    db = loop.run_until_complete(
        aiozmq.rpc.connect_rpc(
            connect=os.environ['DBSERVER_PORT_5000_TCP'],
            translation_table=translation_table,
            timeout=5))

    active_worlds = loop.run_until_complete(db.call.get_active_worlds())
    worlds = {}

    for item in active_worlds:
        world = World(db, events, item['id'])
        loop.run_until_complete(world.init())
        worlds[item['id']] = world

    server_handler = ServerHandler(db, events, worlds)
    server = aiozmq.rpc.serve_rpc(
        server_handler, bind='tcp://0.0.0.0:{}'.format(5200), loop=loop)

    loop.run_until_complete(asyncio.wait([
        server,
        asyncio.async(server_handler.run())
    ]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()

    print("DONE")


if __name__ == '__main__':
    main()
