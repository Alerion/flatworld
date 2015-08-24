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
        self.value = 1
        self.game_value = None
        self.register('get_world', self.get_world)
        self._db = None

    def onOpen(self):
        self._db = yield from aiozmq.rpc.connect_rpc(
            connect=os.environ['DBSERVER_PORT_5000_TCP'],
            translation_table=translation_table,
            timeout=5)
        return
        self._client = yield from aiozmq.rpc.connect_rpc(
            connect='tcp://127.0.0.1:5555',
            timeout=5)

        yield from aiozmq.rpc.serve_pubsub(self, subscribe='events:%s' % self._user['username'], connect='tcp://127.0.0.1:5550')

        topics = ['events', 'messages', 'other']
        i = 0
        while True:
            yield from asyncio.sleep(2)
            i += 1
            topic = random.choice(topics)
            self.publish(topic, i)
            # call RPC
            ret = yield from self._client.call.remote_func(1, i)
            print(self._user['username'], ret)

    # events handlers methods
    @aiozmq.rpc.method
    def set_value(self, value):
        self.game_value = value
        print(self._user['username'], 'set_value', self.game_value)

    # web socker RPC
    # FIXME: Filter private fields
    # FIXME: Add args validation
    @asyncio.coroutine
    def get_world(self, world_id):
        world = yield from self._db.call.get_world(world_id)
        return world


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
