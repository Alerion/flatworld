from django.db import models
from utils.models import JSONField


class Type(models.Model):
    name = models.CharField(max_length=100)
    properties = JSONField(blank=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey(Type)
    parent = models.ForeignKey('self', blank=True, null=True)
    attack = models.PositiveIntegerField()
    defence = models.PositiveIntegerField()
    properties = JSONField(blank=True)
    train_time = models.IntegerField(help_text='in seconds for default speed')
    cost_money = models.IntegerField()
    cost_population = models.IntegerField(default=1)
    cost_iron = models.IntegerField()
    cost_stone = models.IntegerField()
    cost_wood = models.IntegerField()

    def __str__(self):
        return '{}({})[{}/{}]'.format(self.name, self.type, self.attack, self.defence)
