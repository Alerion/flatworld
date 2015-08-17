import asyncio
import aiozmq.rpc
import zmq


class ServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self, *args, **kwargs):
        self.calls = 0
        self.value = 0
        super().__init__(*args, **kwargs)

    @asyncio.coroutine
    def start(self):
        publisher = yield from aiozmq.create_zmq_stream(zmq.PUB, connect='tcp://localhost:5549')

        while True:
            self.value += 1
            print(self.value)
            msg = (str(self.value).encode('utf-8'),)
            publisher.write(msg)
            yield from asyncio.sleep(5)

    @aiozmq.rpc.method
    def remote_func(self, a: int, b: int) -> int:
        self.calls += 1
        print(self.calls, self.value, (a, b))
        return a + b


def main():
    loop = asyncio.get_event_loop()

    server_handler = ServerHandler()

    tasks = [
        asyncio.async(server_handler.start())
    ]

    server = aiozmq.rpc.serve_rpc(
        server_handler, bind='tcp://127.0.0.1:5555', loop=loop)
    tasks.append(server)

    loop.run_until_complete(asyncio.wait(tasks))

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
