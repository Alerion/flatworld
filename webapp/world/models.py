import os

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class World(models.Model):
    name = models.CharField(max_length=100)
    seed = models.DecimalField(max_digits=20, decimal_places=0)
    points = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:world', args=(self.pk,))

    @property
    def mapnik_style_path(self):
        return os.path.join(settings.MAPNIK_STYLES_DIR, 'map_{}.xml'.format(self.pk))

    @property
    def hillshade_path(self):
        return os.path.join(settings.HILLSHADES_DIR, 'map_{}.tif'.format(self.pk))

BIOMES = (
    ('BARE', 'Bare'),
    ('BEACH', 'Beach'),
    ('GRASSLAND', 'Grassland'),
    ('ICE', 'Ice'),
    ('LAKE', 'Lake'),
    ('MARSH', 'Marsh'),
    ('OCEAN', 'OCEAN'),
    ('SCORCHED', 'Scorched'),
    ('SHRUBLAND', 'Shrubland'),
    ('SNOW', 'Snow'),
    ('SUBTROPICAL_DESERT', 'Subtropical deset'),
    ('TAIGA', 'Taiga'),
    ('TEMPERATE_DECIDUOUS_FOREST', 'Deciduous foreset'),
    ('TEMPERATE_DESERT', 'Desert'),
    ('TEMPERATE_RAIN_FOREST', 'Rain forest'),
    ('TROPICAL_RAIN_FOREST', 'Tropical rain forest'),
    ('TROPICAL_SEASONAL_FOREST', 'Tropical seasonal forest'),
    ('TUNDRA', 'Tundra'),
)


class Biome(models.Model):
    border = models.BooleanField()
    coast = models.BooleanField()
    ocean = models.BooleanField()
    water = models.BooleanField()
    river = models.BooleanField()
    biome = models.CharField(max_length=50, choices=BIOMES)
    center = models.PointField(srid=4326)
    elevation = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    moisture = models.FloatField()
    neighbors = models.ManyToManyField('self')
    region = models.ForeignKey('Region', blank=True, null=True)
    world = models.ForeignKey(World)


class River(models.Model):
    geom = models.MultiLineStringField()
    width = models.PositiveIntegerField()
    world = models.ForeignKey(World)


class Region(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=100)
    neighbors = models.ManyToManyField('self')
    world = models.ForeignKey(World)

    def __str__(self):
        return self.name


class City(models.Model):
    biome = models.ForeignKey(Biome)
    capital = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)
    coords = models.PointField(srid=4326)
    world = models.ForeignKey(World)

    def __str__(self):
        return self.name
