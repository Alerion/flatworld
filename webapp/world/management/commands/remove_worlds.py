import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from world.models import World


class Command(BaseCommand):
    help = 'Remove all worlds and related data.'

    def handle(self, *args, **options):
        if input('Do you wish remove all worlds and related data? [y/N]: ') != 'y':
            return

        for name in os.listdir(settings.TILESTACHE_CACHE):
            if name.startswith('map_'):
                path = os.path.join(settings.TILESTACHE_CACHE, name)
                if os.path.isdir(path):
                    shutil.rmtree(path)

        for name in os.listdir(settings.HILLSHADES_DIR):
            if name.endswith('.tif'):
                os.unlink(os.path.join(settings.HILLSHADES_DIR, name))

        for name in os.listdir(settings.MAPNIK_STYLES_DIR):
            if name.endswith('.xml'):
                os.unlink(os.path.join(settings.MAPNIK_STYLES_DIR, name))

        World.objects.all().delete()
        call_command('generate_tilestache_conf')
