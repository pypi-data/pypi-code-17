import random

from .registry import GENERATOR_REGISTRY


def random_int(from_int=0, to_int=999999999):
    return random.randint(from_int, to_int)


GENERATOR_REGISTRY.register(generator_name='random_int', function=random_int)
