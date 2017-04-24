from codeskeleton import exceptions

from .registry import VALIDATOR_REGISTRY


def email(value):
    if '@' not in value:
        raise exceptions.ValueValidationError('Not a valid email address')


VALIDATOR_REGISTRY.register(validator_name='email', function=email)
