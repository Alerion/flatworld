import time
import asyncio
import aiozmq.rpc
import os
import traceback
from zmqrpc.translation_table import translation_table

from engine.engine import WorldEngine


class ServerHandler(aiozmq.rpc.AttrHandler):
    save_treshhold = 30  # seconds

    def __init__(self, loop, db, worlds):
        super().__init__()
        self.worlds = worlds
        self._db = db
        self._loop = loop
        self._last_time = time.time()
        self._tick_time = 1.
        self._from_last_save = 0

    @asyncio.coroutine
    def run(self):
        yield from asyncio.sleep(self._tick_time)

        while True:
            current = time.time()
            elapsed = current - self._last_time
            self._last_time = current

            for world_engine in self.worlds.values():
                yield from world_engine.run(elapsed)

            self._from_last_save += elapsed
            if self._from_last_save > self.save_treshhold:
                self._from_last_save = 0
                for world_engine in self.worlds.values():
                    world = world_engine.get_world()
                    self._db.call.save_world(world)

            yield from asyncio.sleep(current + self._tick_time - time.time())

    @aiozmq.rpc.method
    def get_world(self, world_id: int):
        return self.worlds[world_id].get_world()

    @aiozmq.rpc.method
    def build(self, world_id: int, *args, **kwargs):
        return self.worlds[world_id].build(*args, **kwargs)

    @aiozmq.rpc.method
    def get_city(self, world_id: int, *args, **kwargs):
        return self.worlds[world_id].get_city(*args, **kwargs)


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
        worlds[item['id']] = WorldEngine(loop, events, world)

    server_handler = ServerHandler(loop, db, worlds)
    server = aiozmq.rpc.serve_rpc(
        server_handler, bind='tcp://0.0.0.0:{}'.format(5200),
        translation_table=translation_table, loop=loop,
        log_exceptions=True)

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
