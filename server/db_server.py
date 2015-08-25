import aiopg
import aiozmq.rpc
import asyncio
import os
import psycopg2
from zmqrpc.translation_table import translation_table

if os.environ['DB_PASS']:
    dsn = '''dbname={DB_NAME} user={DB_USER} password={DB_PASS}
 host={DB_PORT_5432_TCP_ADDR} port={DB_PORT_5432_TCP_PORT}'''
else:
    dsn = '''dbname={DB_NAME} user={DB_USER}
 host={DB_PORT_5432_TCP_ADDR} port={DB_PORT_5432_TCP_PORT}'''

dsn = dsn.format(**os.environ)


class DBServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self, pool):
        super().__init__()
        self._pool = pool

    @aiozmq.rpc.method
    @asyncio.coroutine
    def get_world(self, world_id: int):
        with (yield from self._pool.cursor()) as cursor:
            yield from cursor.execute('SELECT * FROM world_world WHERE id=%s', (world_id,))
            world = yield from cursor.fetchone()

            query = '''
            SELECT id, name, world_id, ST_AsGeoJSON(geom) as geom FROM world_region WHERE world_id=%s
            '''
            yield from cursor.execute(query, (world_id,))
            world['regions'] = yield from cursor.fetchall()
            regions_index = {item['id']: item for item in world['regions']}

            query = '''
            SELECT id, name, capital, world_id, region_id, stats, ST_AsGeoJSON(coords) as coords
            FROM world_city WHERE world_id=%s
            '''
            yield from cursor.execute(query, (world_id,))
            cities = yield from cursor.fetchall()
            for city in cities:
                region = regions_index[city['region_id']]
                region.setdefault('cities', []).append(city)

            return world


def main():
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(
        aiopg.create_pool(dsn, cursor_factory=psycopg2.extras.RealDictCursor))
    server = aiozmq.rpc.serve_rpc(
        DBServerHandler(pool),
        bind='tcp://0.0.0.0:5000',
        translation_table=translation_table,
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
