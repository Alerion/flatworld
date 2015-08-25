import aiozmq.rpc
import asyncio
import os
import random
import zmq

from autobahn.asyncio.websocket import WebSocketServerFactory

from rpc import BaseRpcProtocol
from zmqrpc.translation_table import translation_table


class RpcProtocol(BaseRpcProtocol, aiozmq.rpc.AttrHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register('get_world', self.get_world)
        self.register('get_city_stats', self.get_city_stats)
        self.world_id = None
        self._db = None
        self._game = None

    def onConnect(self, request):
        try:
            self.world_id = int(request.params['world_id'][0])
        except (KeyError, ValueError, TypeError, IndexError):
            self.sendClose()

        super().onConnect(request)

    def onOpen(self):
        self._db = yield from aiozmq.rpc.connect_rpc(
            connect=os.environ['DBSERVER_PORT_5000_TCP'],
            translation_table=translation_table,
            timeout=5)

        self._game = yield from aiozmq.rpc.connect_rpc(
            connect=os.environ['GAME_PORT_5200_TCP'],
            timeout=5)

        yield from aiozmq.rpc.serve_pubsub(
            self, subscribe='updates:%s' % self.world_id,
            connect=os.environ['PROXY_PORT_5101_TCP'])

        # topics = ['events', 'messages', 'other']
        # i = 0
        # while True:
        #     yield from asyncio.sleep(2)
        #     i += 1
        #     topic = random.choice(topics)
        #     self.publish(topic, i)
        #     # call RPC
        #     ret = yield from self._client.call.remote_func(1, i)
        #     print(self._user['username'], ret)

    # events handlers methods
    @aiozmq.rpc.method
    def update_cities(self, cities):
        self.publish('update:cities', cities)

    # web socker RPC
    # FIXME: Filter private fields
    # FIXME: Add args validation
    @asyncio.coroutine
    def get_world(self):
        world = yield from self._db.call.get_world(self.world_id)
        return world

    @asyncio.coroutine
    def get_city_stats(self, city_id):
        stats = yield from self._game.call.get_city_stats(self.world_id, city_id)
        return stats


def main():
    factory = WebSocketServerFactory(
        "ws://{}:{}".format(os.environ['FRONTEND_ADDR'], os.environ['FRONTEND_PORT']),
        debug=True)
    factory.protocol = RpcProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', os.environ['FRONTEND_PORT'])
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()

if __name__ == '__main__':
    main()
