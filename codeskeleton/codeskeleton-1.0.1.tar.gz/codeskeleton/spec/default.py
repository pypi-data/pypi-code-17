from codeskeleton import exceptions
from codeskeleton.spec.abstract_spec_object import AbstractSpecObject


class Default(AbstractSpecObject):
    """
    Defines a default value for a :class:`codeskeleton.spec.variable.Variable`.
    """
    def __init__(self, variables, value=None, variable=None):
        """

        Args:
            variables (codeskeleton.spec.variables.Variables): Variables
                available for the ``variable`` argument.
            value: The the default value statically.
            variable (str): The name of a variable to get the default value from.
        """
        self.variables = variables
        self.value = value
        self.variable = variable

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data (dict): A dict like object with one of the following key/value pairs:

                - ``value`` (optional): A static value.
                - ``variable`` (optional): The name of a variable to use as the default value.
        """
        self.value = data.get('value', None)
        self.variable = data.get('variable', None)

    def get_value(self):
        """
        Get the default value.

        If we have a ``value``, return that, otherwise lookup the value
        from the ``variable``.
        """
        if self.value is None:
            return self.variables.get_variable_value(self.variable)
        return self.value

    def validate_spec(self, path):
        if self.value is None and self.variable is None:
            raise exceptions.SpecValidationError(
                path=path,
                message='A default must have "value" or "variable".')
        if self.variable and not self.variables.has_variable(self.variable):
            raise exceptions.SpecValidationError(
                path=path,
                message='Invalid variable referenced by default: {!r}'.format(self.variable))
