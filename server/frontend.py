import aiozmq.rpc
import asyncio
import os
import websocket.rpc

from autobahn.asyncio.websocket import WebSocketServerFactory
from zmqrpc.translation_table import translation_table


class FrontendHandler(websocket.rpc.WebsocketRpc, aiozmq.rpc.AttrHandler):

    def __init__(self, db, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world_id = None
        self._db = db
        self._game = game
        self._pubsub = None

    def onConnect(self, request):
        try:
            self.world_id = int(request.params['world_id'][0])
        except (KeyError, ValueError, TypeError, IndexError):
            self.sendClose()

        super().onConnect(request)

    def onOpen(self):
        self._pubsub = yield from aiozmq.rpc.serve_pubsub(
            self, subscribe='updates:%s' % self.world_id,
            translation_table=translation_table,
            connect=os.environ['PROXY_PORT_5101_TCP'])

    def connection_lost(self, exc):
        self._db = None
        self._game = None
        self._pubsub.close()
        super().connection_lost(exc)

    # events handlers methods
    @aiozmq.rpc.method
    def update_world(self, world):
        self.publish('update:world', world.to_dict())

    # web socker RPC
    # FIXME: Filter private fields
    # FIXME: Add args validation
    @websocket.rpc.method
    @asyncio.coroutine
    def get_world(self):
        world = yield from self._game.call.get_world(self.world_id)
        return world.to_dict()

    @websocket.rpc.method
    @asyncio.coroutine
    def get_city_stats(self, city_id):
        stats = yield from self._game.call.get_city_stats(self.world_id, city_id)
        return stats


def main():
    loop = asyncio.get_event_loop()

    db = loop.run_until_complete(
        aiozmq.rpc.connect_rpc(
            connect=os.environ['DBSERVER_PORT_5000_TCP'],
            translation_table=translation_table,
            timeout=5))

    # Is this good idea to have one connection?
    game = loop.run_until_complete(
        aiozmq.rpc.connect_rpc(
            connect=os.environ['GAME_PORT_5200_TCP'],
            translation_table=translation_table,
            timeout=5))

    def create_protocol(*args, **kwargs):
        return FrontendHandler(db=db, game=game, *args, **kwargs)

    factory = WebSocketServerFactory(
        url='ws://{}:{}'.format(os.environ['FRONTEND_ADDR'], os.environ['FRONTEND_PORT']),
        loop=loop)
    factory.protocol = create_protocol

    server = loop.run_until_complete(
        loop.create_server(factory, '0.0.0.0', os.environ['FRONTEND_PORT']))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()

if __name__ == '__main__':
    main()
