import aiozmq.rpc
import asyncio
import random

from autobahn.asyncio.websocket import WebSocketServerFactory

from rpc import BaseRpcProtocol


class RpcProtocol(BaseRpcProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 1
        self.register('count', self.count)
        self.register('ping', self.ping)
        self.register('get_user', self.get_user)
        self._client = None

    def onOpen(self):
        self._client = yield from aiozmq.rpc.connect_rpc(
            connect='tcp://127.0.0.1:5555',
            timeout=5)

        topics = ['events', 'messages', 'other']
        i = 0
        while True:
            yield from asyncio.sleep(2)
            i += 1
            topic = random.choice(topics)
            self.publish(topic, i)
            # call RPC
            ret = yield from self._client.call.remote_func(1, i)
            print(ret)

    def count(self):
        self.value += 1
        return self.value

    @asyncio.coroutine
    def ping(self, *args):
        yield from asyncio.sleep(3)
        return args

    def get_user(self):
        return self._user


if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://127.0.0.1:9000", debug=True)
    factory.protocol = RpcProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
