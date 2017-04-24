from collections import OrderedDict

from codeskeleton import exceptions
from codeskeleton.spec.abstract_spec_object import AbstractSpecObject
from codeskeleton.spec.variable import Variable


class Variables(AbstractSpecObject):
    """
    Defines variables within a spec.
    """
    def __init__(self, *variables):
        """

        Args:
            *variables: Zero or more :class:`codeskeleton.spec.variable.Variable` objects.
        """
        self._variables = OrderedDict()
        self.add_variables(*variables)

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data (dict): A map object, such as an OrderedDict or a dict. Maps
                variable name to valid data for
                :meth:`codeskeleton.spec.variable.Variable.deserialize`.
        """
        for variable_name, variable_data in data.items():
            variable = Variable(name=variable_name)
            self.add_variable(variable)
            variable.deserialize(variable_data)

    def get_variable(self, variable_name):
        """
        Get the variable object for the provided ``variable_name``.

        Args:
            variable_name (str): Name of the variable to get.

        Raises:
            codeskeleton.exceptions.InvalidVariableName: If no variable with the
                provided ``variable_name`` exists.

        Returns:
            codeskeleton.spec.variable.Variable: The variable.
        """
        try:
            return self._variables[variable_name]
        except KeyError:
            raise exceptions.InvalidVariableName('Invalid variable name: {}'.format(variable_name))

    def get_variable_value(self, variable_name):
        """
        Get the value of the provided ``variable_name``.

        Raises:
            codeskeleton.exceptions.InvalidVariableName: If no variable with the
                provided ``variable_name`` exists.

        Args:
            variable_name (str): Name of the variable to get the value for.
        """
        return self.get_variable(variable_name).get_value()

    def has_variable(self, variable_name):
        """
        Check if we have a variable with a specific ``variable_name``.

        Args:
            variable_name (str): Name of the variable to check for.

        Returns:
            bool: True if we have the variable.
        """
        return variable_name in self._variables

    def set_variable_values(self, **values):
        """
        Set the value of multiple variables.

        Shortcut for calling ``get_varible(variable_name).set_value(value)``
        multiple times.

        Args:
            **values: Variable names mapped to variable values.
        """
        for variable_name, value in values.items():
            variable = self.get_variable(variable_name)
            variable.validate_value(value)
            variable.set_value(value)

    def add_variable(self, variable):
        """
        Add a variable.

        Args:
            variable (codeskeleton.spec.variable.Variable): The variable to add.
        """
        variable.variables = self
        self._variables[variable.name] = variable

    def add_variables(self, *variables):
        """
        Add multiple variables.

        Args:
            *variables: :class:`codeskeleton.spec.variable.Variable` objects.
        """
        for variable in variables:
            self.add_variable(variable)

    def values_as_dict(self):
        """
        Get a dict with all the variables mapped to their values.
        """
        variable_dict = {}
        for variable_name, variable in self._variables.items():
            variable_dict[variable_name] = variable.get_value()
        return variable_dict

    def iterate_input_variables(self):
        """
        Get an iterator over all the variables that takes input.

        This includes all the variables except the ones with a generator.
        """
        for variable in self._variables.values():
            if variable.takes_input():
                yield variable

    def __len__(self):
        """
        Get the number of variables.
        """
        return len(self._variables)

    def __bool__(self):
        return bool(len(self))

    def validate_spec(self, path):
        for variable in self._variables.values():
            variable.validate_spec(path=path)
