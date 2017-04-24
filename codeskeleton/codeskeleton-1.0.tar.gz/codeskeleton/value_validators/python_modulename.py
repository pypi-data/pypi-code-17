import re

from codeskeleton import exceptions

from .registry import VALIDATOR_REGISTRY


def python_modulename(value):
    if not re.match(r'^[a-z][a-z0-9_]+[a-z0-9]$', value):
        raise exceptions.ValueValidationError(
            'Must be all lowercase, start with a-z, end with a-z or a number, and the '
            'characters between the first and last characters can only be a-z numbers or _.')


VALIDATOR_REGISTRY.register(validator_name='python_modulename', function=python_modulename)
