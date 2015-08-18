from django.contrib.gis.db import models


class World(models.Model):
    name = models.CharField(max_length=100)
    seed = models.DecimalField(max_digits=20, decimal_places=0)
    points = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)


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
    lat = models.FloatField()
    lng = models.FloatField()
    biome = models.CharField(max_length=50, choices=BIOMES)
    elevation = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    moisture = models.FloatField()
    neighbors = models.ManyToManyField('self')
    region = models.ForeignKey('Region')


class River(models.Model):
    geom = models.MultiLineStringField()
    width = models.PositiveIntegerField()


class Region(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=100)
    neighbors = models.ManyToManyField('self')
    capital = models.OneToOneField('City', related_name='capital_of')

    def __str__(self):
        return self.name


class City(models.Model):
    biome = models.ForeignKey(Biome)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name
