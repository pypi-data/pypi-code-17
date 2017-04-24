from collections import OrderedDict

from codeskeleton import exceptions
from codeskeleton import value_validators
from codeskeleton.spec.abstract_spec_object import AbstractSpecObject


class ValueValidators(AbstractSpecObject):

    def __init__(self, validators=None):
        self._validators = OrderedDict(validators or {})

    def deserialize(self, data):
        self._validators = OrderedDict(data.items())

    def validate_value(self, value):
        for validator_name in self._validators:
            value_validators.VALIDATOR_REGISTRY.validate_value(validator_name=validator_name,
                                                               value=value)

    def validate_spec(self, path):
        for validator_name in self._validators:
            if validator_name in value_validators.VALIDATOR_REGISTRY:
                raise exceptions.SpecValidationError(
                    path=path,
                    message='Invalid value validator: {!r}. Must be one of: {}'.format(
                        validator_name, ', '.join(value_validators.VALIDATOR_REGISTRY.namelist())))

    def __len__(self):
        return len(self._validators)
