import random

from .registry import GENERATOR_REGISTRY


def make_random_string(allowed_characters, length):
    return ''.join(random.SystemRandom().choice(allowed_characters) for i in range(length))


GENERATOR_REGISTRY.register(generator_name='make_random_string', function=make_random_string)
