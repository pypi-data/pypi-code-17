from codeskeleton.value_generators.make_random_string import make_random_string
from .registry import GENERATOR_REGISTRY


def django_secret_key(length=50):
    allowed_characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return make_random_string(allowed_characters=allowed_characters,
                              length=length)


GENERATOR_REGISTRY.register(generator_name='django_secret_key', function=django_secret_key)
