from django.db import models

from server.engine.models.building import properties_schema
from utils.models import JSONField


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def max_level(self):
        return self.buildingtier_set.order_by('-level').first().level


class BuildingTier(models.Model):
    building = models.ForeignKey(Building)
    level = models.PositiveSmallIntegerField(default=1)
    build_time = models.IntegerField(help_text='in seconds for default speed')
    cost_money = models.IntegerField()
    cost_population = models.IntegerField()
    cost_iron = models.IntegerField()
    cost_stone = models.IntegerField()
    cost_wood = models.IntegerField()
    properties = JSONField(schema=properties_schema)

    class Meta:
        unique_together = ('building', 'level')
