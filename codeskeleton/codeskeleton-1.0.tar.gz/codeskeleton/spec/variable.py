import codeskeleton
from codeskeleton import exceptions
from codeskeleton import value_generators
from codeskeleton.spec.abstract_spec_object import AbstractSpecObject
from codeskeleton.spec.default import Default
from codeskeleton.spec.value_validators import ValueValidators


class Variable(AbstractSpecObject):
    """
    Defines a variable.
    """
    def __init__(self, name, variables=None, default=None,
                 help_text=None, generator=None, arguments=None,
                 validators=None,
                 value=None):
        """

        Args:
            name (str): Name of the variable.
            variables (codeskeleton.spec.variables.Variables): Variables
                available a ``default`` for the variable (see ``default`` below).
            default (codeskeleton.spec.default.Default): The default value
                for the variable.
            help_text (str): Help text for users setting the variable.
            generator (str): The name of a value generator. See
                :class:`codeskeleton.value_generators.registry.ValueGeneratorRegistry`.
                If this is provided, the variable gets the value from a generator
                function instead of from user input.
            arguments (dict): Arguments for the ``generator`` function.
            validators (list): A list mapping validator function names to
                arguments for the validator function. See
                :class:`codeskeleton.value_validators.registry.ValueValidatorRegistry`.
            value: Set a value. Normally only used when writing tests, since values
                come from user input.
        """
        self.variables = variables
        self.name = name
        self.default = default
        self.help_text = help_text
        self.generator = generator
        self.arguments = arguments
        self.value = value
        self.validators = validators or ValueValidators()

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data (dict): A dict like object with one of the following key/value pairs:

                - ``default`` (optional): A dict with valid data for
                    :meth:`codeskeleton.spec.default.Default.deserialize`.
                - ``validators`` (optional): A dict mapping the name of a validator in
                  :obj:`codeskeleton.value_validators.registry.VALIDATOR_REGISTRY`
                  to kwargs for the validator.
                - ``generator`` (optional): The name of a generator in
                  :obj:`codeskeleton.value_generators.registry.GENERATOR_REGISTRY`.
                - ``arguments`` (optional): Dict with arguments for the ``generator``
                  function.
                - ``help_text`` (optional): String with help text for users setting the variable.
        """
        if 'default' in data:
            self.default = Default(variables=self.variables)
            self.default.deserialize(data['default'])
        else:
            self.default = None
        self.validators = ValueValidators()
        if 'validators' in data:
            self.validators.deserialize(data['validators'])
        self.help_text = data.get('help_text', None)
        self.generator = data.get('generator', None)
        self.arguments = data.get('arguments', None)

    def is_required(self):
        """
        Is this variable required?

        Does not make sense unless :meth:`.takes_input` returns ``False``.

        Returns:
            bool: ``True`` if the variable has no default.
        """
        return self.default is None

    def takes_input(self):
        """
        Does this variable require user input?


        Returns:
            bool: ``True`` if the variable has a ``generator``.
        """
        return self.generator is None

    def set_value(self, value):
        """
        Set the value of the variable.

        Should be used after using :meth:`.validate_value` to
        validate the value.

        Args:
            value: The value to set for the variable.
        """
        self.value = value

    def get_value(self):
        """
        Get the value of the variable.

        Lookup happens in this order:

        - If the variable has a value (see :meth:`.set_value`), return the value.
        - If the variable has a ``default``, use :meth:`codeskeleton.spec.default.Default.get_value`.
        - If the variable has a ``generator``, call the generator function to get the value.

        Raises:
            codeskeleton.exceptions.VariableSpecError: If the variable does not have any
               of ``value``, ``default`` or ``generator``.
        """
        if self.value is not None:
            return self.value
        if self.default:
            return self.default.get_value()
        if self.generator:
            kwargs = self.arguments or {}
            return value_generators.GENERATOR_REGISTRY.generate_value(self.generator, **kwargs)
        raise Exception('Found a required value but no value. Did you forget to '
                        'use validate_value() before calling get_value()?')

    def validate_spec(self, path):
        if self.generator and self.default:
            raise exceptions.SpecValidationError(
                path=path,
                message='Can not provide both "default" and "generator".')
        if self.generator and self.generator not in value_generators.GENERATOR_REGISTRY:
            raise exceptions.SpecValidationError(
                path=path,
                message='Invalid generator: {!r}. Must be one of: {}'.format(
                    self.generator, ', '.join(value_generators.GENERATOR_REGISTRY.namelist())))
        if self.arguments and not self.generator:
            raise exceptions.SpecValidationError(
                path=path,
                message='Can not use "arguments" without a "generator".')

    def validate_value(self, value):
        """
        Validate the provided value using all the validators specified for this variable.

        Should be used before using :meth:`.set_value`.

        Args:
            value: Value to validate.

        Raises:
            codeskeleton.exceptions.ValueValidationError: If validation fails.
        """
        self.validators.validate_value(value=value)
