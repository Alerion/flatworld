from django.db import models
from utils.models import JSONField


class Quest(models.Model):
    world = models.ForeignKey('world.World')
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    # When it become available
    created = models.DateTimeField()
    # When it become unavailable
    finished = models.DateTimeField(blank=True, null=True)
    # It is active till this time or till finished
    last_till = models.DateTimeField(blank=True, null=True)
    # Can user join quest few times?
    repeatable = models.BooleanField(default=False)
    # Should we resolve quest even if user does not join it?
    required = models.BooleanField(default=False)

    duration = models.IntegerField()
    start_position = models.IntegerField(default=-100)
    roll_width = models.IntegerField(default=100)
    results = JSONField()
    requirements = JSONField(blank=True)

    # If these are blank, any one can join this quest
    cities = models.ManyToManyField('world.City', blank=True)
    regions = models.ManyToManyField('world.Region', blank=True)

    def __str__(self):
        return self.name


class Participation(models.Model):
    quest = models.ForeignKey(Quest)
    city = models.ForeignKey('world.City')
    joined = models.DateTimeField()
    finished = models.DateTimeField(blank=True, null=True)
    outfit = JSONField(blank=True)
    result_roll = models.PositiveIntegerField(blank=True, null=True)
    loot = JSONField(blank=True)
