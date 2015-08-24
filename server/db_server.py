import aiopg
import aiozmq.rpc
import asyncio
import os

if os.environ['DB_PASS']:
    dsn = '''dbname={DB_NAME} user={DB_USER} password={DB_PASS}
 host={DB_PORT_5432_TCP_ADDR} port={DB_PORT_5432_TCP_PORT}'''
else:
    dsn = '''dbname={DB_NAME} user={DB_USER}
 host={DB_PORT_5432_TCP_ADDR} port={DB_PORT_5432_TCP_PORT}'''

dsn = dsn.format(**os.environ)


class DBServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self):
        super().__init__()
        self._pool = None

    def pool(self):
        pass

    @aiozmq.rpc.method
    def get_world(self, world_id: int):
        with (yield from self._pool.cursor()) as cur:
            yield from cur.execute('SELECT * FROM world_world')
            result = yield from cur.fetchone()
            print(result)
            return result


def main():
    loop = asyncio.get_event_loop()
    server = aiozmq.rpc.serve_rpc(
        DBServerHandler(),
        bind='tcp://0.0.0.0:5000',
        loop=loop)
    loop.run_until_complete(server)

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
