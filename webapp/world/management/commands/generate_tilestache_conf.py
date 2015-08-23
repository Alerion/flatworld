from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from world.models import World


class Command(BaseCommand):
    help = 'Generate Tile Stache config.'

    def handle(self, *args, **kwargs):
        context = {
            'worlds': World.objects.all(),
            'TILESTACHE_CACHE': settings.TILESTACHE_CACHE
        }
        with open(settings.TILESTACHE_CONF_PATH, 'w') as conf:
            conf.write(render_to_string(settings.TILESTACHE_CONF_TEMPLATE, context))
