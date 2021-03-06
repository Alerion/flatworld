class RequestError(Exception):
    """Error raised from RPC method and send as error to client."""

    def __init__(self, errors):
        self.errors = errors


class CityDoesNotExist(RequestError):

    def __init__(self, city_id):
        self.city_id = city_id
        super().__init__({
            'city_does_not_exist': 'City with ID {} does not exist'.format(city_id)
        })


class BuildingDoesNotExist(RequestError):

    def __init__(self, building_id):
        self.building_id = building_id
        super().__init__({
            'building_does_not_exist': 'Building with ID {} does not exist'.format(building_id)
        })


class BuildError(RequestError):

    def __init__(self, city_id, building_id, message):
        self.city_id = city_id
        self.building_id = building_id
        super().__init__({
            'build_error': message
        })


class QuestDoesNotExist(RequestError):

    def __init__(self, quest_id, city_id=None):
        self.quest_id = quest_id
        self.city_id = city_id
        super().__init__({
            'quest_does_not_exist': 'Quest with ID {} does not exist'.format(quest_id)
        })


class QuestError(RequestError):

    def __init__(self, quest_id, city_id, message):
        self.quest_id = quest_id
        self.city_id = city_id
        super().__init__({
            'quest_error': message
        })
