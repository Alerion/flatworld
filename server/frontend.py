import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory

from rpc import BaseRpcProtocol, register


class RpcProtocol(BaseRpcProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 1
        self.register('count', self.count)
        self.register('ping', self.ping)

    def count(self):
        self.value += 1
        return self.value

    @asyncio.coroutine
    def ping(self, *args):
        yield from asyncio.sleep(5)
        return args


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

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
