from codeskeleton import exceptions

from .registry import VALIDATOR_REGISTRY


def one_letter(value):
    if len(str(value)) != 1:
        raise exceptions.ValueValidationError('Must be exactly one letter')


VALIDATOR_REGISTRY.register(validator_name='one_letter', function=one_letter)
