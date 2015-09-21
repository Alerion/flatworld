import os
import shutil

from django.core.management.base import BaseCommand

from server.engine.models import DEFAULT_WORLD_PARAMS
from world.models import World


class Command(BaseCommand):
    help = 'Reset world and all cities.'

    def add_arguments(self, parser):
        parser.add_argument('--world_id', action="store", dest="world_id", type=int)

    def handle(self, world_id, *args, **options):
        world = World.objects.get(pk=world_id)

        world.params.update(DEFAULT_WORLD_PARAMS)
        world.save()

        for city in world.city_set.all():
            city.reset()
            city.save()
