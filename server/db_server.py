import aiopg
import aiozmq.rpc
import asyncio
import os
import psycopg2
from zmqrpc.translation_table import translation_table

from engine import models
from engine.base import ModelsDict

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

    @asyncio.coroutine
    def _load_world(self, world_id, cursor):
        query = '''
        SELECT id, name, params, created FROM world_world WHERE id=%s
        '''
        yield from cursor.execute(query, (world_id,))
        data = yield from cursor.fetchone()
        return models.World(data)

    @asyncio.coroutine
    def _load_regions(self, world, cursor):
        query = '''
        SELECT *, ST_AsGeoJSON(geom) as geom FROM world_region WHERE world_id=%s
        '''
        yield from cursor.execute(query, (world.id,))
        data = yield from cursor.fetchall()

        query = '''
        SELECT rn.from_region_id AS region_id, array_agg(rn.to_region_id) AS neighbors
        FROM world_region_neighbors rn JOIN world_region r ON (rn.from_region_id=r.id)
        WHERE r.world_id=%s GROUP BY from_region_id
        '''
        yield from cursor.execute(query, (world.id,))
        neighbors_data = yield from cursor.fetchall()

        regions = {}
        for item in data:
            region = models.Region(item, world=world)
            regions[region.id] = region

        for item in neighbors_data:
            for neighbor_id in item['neighbors']:
                regions[item['region_id']].neighbors[neighbor_id] = regions[neighbor_id]

        world.regions = regions

    @asyncio.coroutine
    def _load_cities(self, world, cursor):
        query = '''
        SELECT *, ST_AsGeoJSON(coords) as coords FROM world_city WHERE world_id=%s
        '''
        yield from cursor.execute(query, (world.id,))
        data = yield from cursor.fetchall()

        for item in data:
            region = world.regions[item['region_id']]
            city = models.City(item, world=world, region=region)
            region.cities[city.id] = city

    @aiozmq.rpc.method
    @asyncio.coroutine
    def get_world(self, world_id: int):
        with (yield from self._pool.cursor()) as cursor:
            world = yield from self._load_world(world_id, cursor)
            yield from self._load_regions(world, cursor)
            yield from self._load_cities(world, cursor)
            return world

    @aiozmq.rpc.method
    @asyncio.coroutine
    def get_active_worlds(self):
        with (yield from self._pool.cursor()) as cursor:
            yield from cursor.execute('SELECT id FROM world_world')
            worlds = yield from cursor.fetchall()
            return worlds

    @aiozmq.rpc.method
    @asyncio.coroutine
    def get_buildings(self):
        with (yield from self._pool.cursor()) as cursor:
            yield from cursor.execute('SELECT * FROM building_building')
            data = yield from cursor.fetchall()
            buildings = ModelsDict()
            for item in data:
                buildings[item['id']] = models.Building(item)
            print(type(buildings))
            return buildings


def main():
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(
        aiopg.create_pool(dsn, cursor_factory=psycopg2.extras.RealDictCursor))
    handler = DBServerHandler(pool)
    server = aiozmq.rpc.serve_rpc(
        handler,
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
