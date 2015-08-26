"""
Keep these objects as simple as possible. They are passed via 0MQ with Pickle.
"""
# FIXME: WORLD_PARAMS is used in generate_world command. Not sure this is the best place,
# because requires to add the main folder to python paths.
DEFAULT_WORLD_PARAMS = {
    'start_population': 2000,
    'base_population_growth': 0.05,
    'points': None,
    'seed': None
}


class WorldParams:

    def __init__(self, **kwargs):
        for field in DEFAULT_WORLD_PARAMS:
            setattr(self, field, kwargs[field])

    def to_json(self):
        output = {}
        for field in DEFAULT_WORLD_PARAMS:
            output[field] = getattr(self, field)
        return output


class World:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.created = kwargs['created']
        self.name = kwargs['name']
        self.params = WorldParams(**kwargs['params'])

        self.cities = {}
        self.regions = {}


class Region:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

        self.world = kwargs['world']
        self.neighbors = {}


class CityStats:

    def __init__(self, **kwargs):
        self.population = kwargs['population']
        self.population_growth = kwargs['population_growth']


class City:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.capital = kwargs['capital']
        self.coords = kwargs['coords']
        self.name = kwargs['name']
        self.stats = CityStats(**kwargs['stats'])

        self.region = kwargs['region']
        self.world = kwargs['world']
