from codeskeleton.value_generators.make_random_string import make_random_string
from .registry import GENERATOR_REGISTRY


def debug(suffix=''):
    """
    Generator just for debugging.

    Returns:
        str: The string ``DEBUG`` suffixed with the provided ``suffix``.
    """
    return 'DEBUG{}'.format(suffix)


GENERATOR_REGISTRY.register(generator_name='debug', function=debug)
