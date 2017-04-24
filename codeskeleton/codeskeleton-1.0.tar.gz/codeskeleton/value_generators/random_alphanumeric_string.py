from codeskeleton.value_generators.make_random_string import make_random_string
from .registry import GENERATOR_REGISTRY


def random_alphanumeric_string(length):
    allowed_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return make_random_string(allowed_characters=allowed_characters,
                              length=length)


GENERATOR_REGISTRY.register(generator_name='random_alphanumeric_string', function=random_alphanumeric_string)
