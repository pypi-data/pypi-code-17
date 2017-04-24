class ValueValidatorRegistry(object):
    """
    Registry of validators for
    :class:`codeskeleton.spec.variable.Variable`.
    """
    def __init__(self):
        self.validators = {}

    def register(self, validator_name, function):
        """
        Register a validator function.

        Args:
            validator_name (str): The name of the validator.
            function: The validator function. The validator function
                must raise :exc:`codeskeleton.exceptions.ValueValidationError`
                if validation fails.
        """
        self.validators[validator_name] = function

    def validate_value(self, validator_name, value):
        """
        Validate a value.

        Args:
            validator_name (str): Name of the validator to execute.
            value: The value to validate.

        Raises:
            codeskeleton.exceptions.ValueValidationError: If validation fails.
        """
        self.validators[validator_name](value=value)

    def __contains__(self, validator_name):
        """
        Returns ``True`` if we have a validator with the provided ``validator_name`` in the registry.
        """
        return validator_name in self.validators

    def namelist(self):
        """
        Get the names of all validators in the registry as a list of strings.
        """
        return list(self.validators.keys())


#: The validator registry. Use this to access the validator registry
#: (do not create a new :class:`.ValueValidatorRegistry` object.
VALIDATOR_REGISTRY = ValueValidatorRegistry()
