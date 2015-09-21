import aiopg
import aiozmq.rpc
import asyncio
import os
import psycopg2
from psycopg2.extras import Json
from zmqrpc.translation_table import translation_table

from engine import models
from engine.models.base import ModelsDict
import pprint
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
        world = models.World(data)
        buildings = yield from self.get_buildings()
        world.buildings = buildings
        return world

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
            item['buildings'] = item['buildings'] or {}

            # fix buildings keys
            new_buildings = {}
            for key, value in item['buildings'].items():
                new_buildings[int(key)] = value
            item['buildings'] = new_buildings

            # Fill building that does not exist. This may happen if new building was added
            for building_id in world.buildings.keys():
                if building_id not in item['buildings']:
                    item['buildings'][building_id] = {
                        'level': 0,
                        'in_progress': False,
                        'building_id': building_id,
                        'build_progress': 0
                    }

            city = models.City(item, world=world, region=region)
            region.cities[city.id] = city
            world.cities[city.id] = city

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
            yield from cursor.execute('SELECT * FROM building_buildingtier ORDER BY level')
            data = yield from cursor.fetchall()
            building_tiers = {}
            for row in data:
                building_tiers.setdefault(row['building_id'], {})[row['level']] = row

            yield from cursor.execute('SELECT * FROM building_building')
            data = yield from cursor.fetchall()
            buildings = ModelsDict()
            for row in data:
                row['tiers'] = building_tiers[row['id']]
                buildings[row['id']] = models.Building(row)

            return buildings

    @aiozmq.rpc.method
    @asyncio.coroutine
    def get_user_data(self, user_id: int):
        with (yield from self._pool.cursor()) as cursor:
            yield from cursor.execute('SELECT id FROM world_city WHERE user_id=%s', (user_id,))
            data = yield from cursor.fetchone()
            return {
                'city_id': data['id']
            }

    @aiozmq.rpc.method
    @asyncio.coroutine
    def save_world(self, world):
        with (yield from self._pool.cursor()) as cursor:
            for city in world.cities.values():
                data = city.to_dict(with_initial=True)
                yield from cursor.execute(
                    'UPDATE world_city SET buildings=%s, stats=%s WHERE id=%s',
                    (Json(data['buildings']), Json(data['stats']), city.id))


def main():
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(
        aiopg.create_pool(dsn, cursor_factory=psycopg2.extras.RealDictCursor))
    handler = DBServerHandler(pool)
    server = aiozmq.rpc.serve_rpc(
        handler,
        bind='tcp://0.0.0.0:5000',
        translation_table=translation_table,
        loop=loop,
        log_exceptions=True)
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
