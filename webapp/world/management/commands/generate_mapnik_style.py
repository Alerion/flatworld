from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from world.models import World


class Command(BaseCommand):
    help = 'Generate Mapnik style for worlds'

    def add_arguments(self, parser):
        parser.add_argument('--world', action="store", dest="world", type=int, default=None)

    def handle(self, world, *args, **kwargs):
        if world is None:
            for obj in World.objects.all():
                self.generate_style(obj)
        else:
            try:
                obj = World.objects.get(pk=world)
                self.generate_style(obj)
            except World.DoesNotExist:
                raise CommandError('World with ID {} does not exist.'.format(world))

    def generate_style(self, obj):
        with open(obj.mapnik_style_path, 'w') as style_file:
            context = {
                'world': obj,
                'DB': settings.DATABASES['default']
            }
            style_file.write(render_to_string(settings.MAPNIK_STYLE_TEMPLATE, context))
