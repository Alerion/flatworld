import random
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from map import generators, exports
from map.map import Map
from world.models import Biome, River, Region, City, World


class Command(BaseCommand):
    help = 'Generate new world'

    def add_arguments(self, parser):
        parser.add_argument('--max_lat', action="store", dest="max_lat", type=int, default=70)
        parser.add_argument('--max_lng', action="store", dest="max_lng", type=int, default=70)
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

        world = World(seed=seed, name='World#{}'.format(seed), points=points)
        world.save()

        hillshade_path = os.path.join(settings.HILLSHADES_DIR, 'map_{}.tif'.format(world.pk))

        map_obj = Map(seed, [
            generators.points.RelaxedPoints(points_number=points).generate,
            generators.graph.VoronoiGraph().generate,
            generators.graph.VoronoiGraph().imporove_corners,
            generators.land.SimplexIsland().generate,
            generators.elevation.FromCoast().generate,
            generators.rivers.RandomRiver().generate,
            generators.biomes.Moisture().generate,
            generators.regions.HexGrid().generate,
            Exporter(
                world, Biome, River, Region, City, max_lat=max_lat, max_lng=max_lng).export,
            exports.GeoTiffExporter(
                max_lat, max_lng, heights_map_width, hill_noise, hillshade_path).export,
        ])

        map_obj.generate()


class Exporter(exports.ModelExporter):

    def __init__(self, world, *args, **kwargs):
        self.world = world
        super().__init__(*args, **kwargs)

    def biome_pre_save(self, obj, center, map_obj):
        obj.world = self.world

    def city_pre_save(self, obj, city, map_obj):
        obj.world = self.world

    def region_pre_save(self, obj, region, map_obj):
        obj.world = self.world

    def river_pre_save(self, obj, edge, map_obj):
        obj.world = self.world

    def cleanup_biome(self, map_obj):
        self.biome_model.objects.filter(world=self.world).delete()

    def cleanup_city(self, map_obj):
        self.city_model.objects.filter(world=self.world).delete()

    def cleanup_region(self, map_obj):
        self.region_model.objects.filter(world=self.world).delete()

    def cleanup_river(self, map_obj):
        self.river_model.objects.filter(world=self.world).delete()
