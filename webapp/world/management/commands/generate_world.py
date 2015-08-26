import random

from django.core.management import call_command
from django.core.management.base import BaseCommand

from world import generators, exports
from world.map import Map
from world.models import Biome, River, Region, City, World

from server.engine.models import DEFAULT_WORLD_PARAMS


class Command(BaseCommand):
    help = 'Generate new world'

    def add_arguments(self, parser):
        parser.add_argument('--max_lat', action="store", dest="max_lat", type=int, default=60)
        parser.add_argument('--max_lng', action="store", dest="max_lng", type=int, default=60)
        parser.add_argument('--seed', action="store", dest="seed", type=int)
        parser.add_argument('--points', action="store", dest="points", type=int, default=1000)
        parser.add_argument(
            '--hill_noise', action="store", dest="hill_noise", type=bool, default=False)
        parser.add_argument(
            '--heights_map_width', action="store", dest="heights_map_width", type=int,
            default=1000)

    def handle(self, max_lat, max_lng, seed, points, hill_noise, heights_map_width,
               *args, **options):
        if seed is None:
            seed = int(random.random() * 10000)
        print('seed = %s' % seed)

        params = dict(DEFAULT_WORLD_PARAMS)
        params['seed'] = seed
        params['points'] = points
        world = World(name='World#{}'.format(seed), params=params)
        world.save()

        map_obj = Map(seed, [
            generators.points.RelaxedPoints(points_number=points).generate,
            generators.graph.VoronoiGraph().generate,
            generators.graph.VoronoiGraph().imporove_corners,
            generators.land.SimplexIsland().generate,
            generators.elevation.FromCoast().generate,
            generators.rivers.RandomRiver().generate,
            generators.biomes.Moisture().generate,
            generators.regions.HexGrid().generate,
            exports.ModelExporter(
                world, Biome, River, Region, City, max_lat=max_lat, max_lng=max_lng).export,
            exports.GeoTiffExporter(
                max_lat, max_lng, heights_map_width, hill_noise, world.hillshade_path).export,
        ])

        map_obj.generate()
        call_command('generate_mapnik_style', world=world.pk)
        call_command('generate_tilestache_conf')
