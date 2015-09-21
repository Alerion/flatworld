from .base import Model
from . import fields


class Type(Model):
    id = fields.IntegerField()
    name = fields.CharField()


class Unit(Model):
    id = fields.IntegerField()
    name = fields.CharField()
    description = fields.CharField()
    type = fields.ModelField(Type)
    parent_id = fields.IntegerField()
    attack = fields.IntegerField()
    defence = fields.IntegerField()
    properties = fields.JSONField()
    train_time = fields.IntegerField()
    cost_money = fields.IntegerField()
    cost_population = fields.IntegerField()
    cost_iron = fields.IntegerField()
    cost_stone = fields.IntegerField()
    cost_wood = fields.IntegerField()
