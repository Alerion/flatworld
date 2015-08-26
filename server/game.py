import asyncio
import aiozmq.rpc
import os
from zmqrpc.translation_table import translation_table

from engine.engine import WorldEngine


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
            for world_engine in self.worlds.values():
                world_engine.run()

            yield from asyncio.sleep(130)

            # self.value += 1
            # print(self.value)
            # self._events.publish('updates:{}'.format(self.world_id)).set_value(self.value)

    @aiozmq.rpc.method
    def get_city_stats(self, world_id: int, city_id: int):
        return self.worlds[world_id].get_city_stats(city_id)

    @aiozmq.rpc.method
    def get_world(self, world_id: int):
        return self.worlds[world_id].get_world()


def main():
    loop = asyncio.get_event_loop()

    events = loop.run_until_complete(
        aiozmq.rpc.connect_pubsub(
            connect=os.environ['PROXY_PORT_5100_TCP'],
            translation_table=translation_table))

    db = loop.run_until_complete(
        aiozmq.rpc.connect_rpc(
            connect=os.environ['DBSERVER_PORT_5000_TCP'],
            translation_table=translation_table,
            timeout=5))

    active_worlds = loop.run_until_complete(db.call.get_active_worlds())
    worlds = {}

    for item in active_worlds:
        world_engine = WorldEngine(db, events, item['id'])
        loop.run_until_complete(world_engine.init())
        worlds[item['id']] = world_engine

    server_handler = ServerHandler(db, events, worlds)
    server = aiozmq.rpc.serve_rpc(
        server_handler, bind='tcp://0.0.0.0:{}'.format(5200),
        translation_table=translation_table, loop=loop)

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
