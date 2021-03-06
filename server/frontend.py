import aiozmq.rpc
import asyncio
import os
import websocket.rpc

from websocket.rpc import RequestError

from autobahn.asyncio.websocket import WebSocketServerFactory
from zmqrpc.translation_table import translation_table, error_table


class FrontendHandler(websocket.rpc.WebsocketRpc, aiozmq.rpc.AttrHandler):

    def __init__(self, db, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world_id = None
        self.city_id = None
        self._db = db
        self._game = game
        self._pubsub = None
        self._city_pubsub = None

    def onConnect(self, request):
        try:
            self.world_id = int(request.params['world_id'][0])
        except (KeyError, ValueError, TypeError, IndexError):
            self.sendClose()

        super().onConnect(request)

    def onOpen(self):
        user_data = yield from self._db.call.get_user_data(self._user['id'])
        self.city_id = user_data['city_id']

        self._pubsub = yield from aiozmq.rpc.serve_pubsub(
            self, subscribe='updates:world:%s' % self.world_id,
            translation_table=translation_table,
            connect=os.environ['PROXY_PORT_5101_TCP'])

        self._city_pubsub = yield from aiozmq.rpc.serve_pubsub(
            self, subscribe='updates:city:%s' % self.city_id,
            translation_table=translation_table,
            connect=os.environ['PROXY_PORT_5101_TCP'])

    def connection_lost(self, exc):
        self._db = None
        self._game = None
        self._pubsub.close()
        self._city_pubsub.close()
        super().connection_lost(exc)

    # events handlers methods
    @aiozmq.rpc.method
    def update_world(self, world):
        city = world.cities.get(self.city_id)
        self.publish('update:city', city.to_dict(detailed=True))
        self.publish('update:world', world.to_dict())

    @aiozmq.rpc.method
    def update_quests(self, quests):
        self.publish('update:quests', quests.to_dict())

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
    def get_city(self):
        city = yield from self._game.call.get_city(self.world_id, self.city_id)
        return city.to_dict(detailed=True)

    @websocket.rpc.method
    @asyncio.coroutine
    def get_units(self):
        units = yield from self._db.call.get_units()
        return units.to_dict()

    @websocket.rpc.method
    @asyncio.coroutine
    def get_buildings(self):
        buildings = yield from self._db.call.get_buildings()
        return buildings.to_dict()

    @websocket.rpc.method
    @asyncio.coroutine
    def get_quests(self):
        quests = yield from self._game.call.get_quests(self.world_id, self.city_id)
        return quests.to_dict()

    @websocket.rpc.method
    @asyncio.coroutine
    def build(self, building_id):
        city = yield from self._game.call.build(self.world_id, self.city_id, building_id)
        return city.to_dict(detailed=True)

    @websocket.rpc.method
    @asyncio.coroutine
    def start_quest(self, quest_id):
        city = yield from self._game.call.start_quest(self.world_id, self.city_id, quest_id)
        return city.to_dict(detailed=True)

    @websocket.rpc.method
    @asyncio.coroutine
    def close_quest(self, quest_id):
        city = yield from self._game.call.close_quest(self.world_id, self.city_id, quest_id)
        return city.to_dict(detailed=True)


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
            error_table=error_table,
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
