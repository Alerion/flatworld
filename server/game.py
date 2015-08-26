import time
import asyncio
import aiozmq.rpc
import os
from zmqrpc.translation_table import translation_table

from engine.engine import WorldEngine


class ServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self, worlds, db, events):
        super().__init__()
        self.worlds = worlds
        self._db = db
        self._events = events
        self._last_time = time.time()
        self._tick_time = 1.

    @asyncio.coroutine
    def run(self):
        yield from asyncio.sleep(self._tick_time)

        while True:
            current = time.time()
            elapsed = current - self._last_time
            self._last_time = current

            for world_engine in self.worlds.values():
                yield from world_engine.run(elapsed)

            yield from asyncio.sleep(current + self._tick_time - time.time())

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
        world = loop.run_until_complete(db.call.get_world(item['id']))
        worlds[item['id']] = WorldEngine(events, world)

    server_handler = ServerHandler(worlds, db, events)
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
