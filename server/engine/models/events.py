from datetime import datetime, timezone

from . import fields
from .base import Model


class QuestResult(Model):
    roll_point = fields.IntegerField()
    type = fields.CharField()
    reward = fields.JSONField()


class Quest(Model):
    id = fields.IntegerField()
    world_id = fields.IntegerField()
    name = fields.CharField()
    description = fields.CharField()
    # When it become available
    created = fields.DateTimeField()
    # When it become unavailable
    finished = fields.DateTimeField()
    # It is active till this time or till finished
    last_till = fields.DateTimeField()
    # Can user join quest few times?
    repeatable = fields.BooleanField()
    # Should we resolve quest even if user does not join it?
    required = fields.BooleanField()

    duration = fields.IntegerField()
    start_position = fields.IntegerField()
    roll_width = fields.IntegerField()
    results = fields.ModelCollectionField(QuestResult)
    requirements = fields.JSONField()

    # If these are blank, any one can join this quest
    cities = fields.FieldCollectionField(fields.IntegerField())
    regions = fields.FieldCollectionField(fields.IntegerField())

    def is_private_for_city(self, city):
        if len(self.cities) != 1:
            return False

        if self.regions:
            return False

        return self.cities[0] == city.id

    def finish(self):
        self.finished = datetime.now(timezone.utc)
