"""
Sets environment variables in the Docker image
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class EnvironmentOperation(Operation):
    """
    Operation that sets environment variables
    """

    variables: typing.Dict[str, typing.Any]

    def __init__(self, variables: typing.Dict[str, typing.Any]) -> None:
        """
        Creates an enviornment operation instance
        """

        self.variables = variables

    def build(self) -> str:
        variables = ' \\\n    '.join(
            [
                f'{key}={value}'
                for key, value in self.variables.items()
            ]
        )

        return f'ENV {variables}'
# pylint: enable=too-few-public-methods

# pylint: disable=bad-whitespace
def environment(
        image,
        key: typing.Union[str, typing.Dict[str, typing.Any]],
        value: typing.Union[typing.Any, None] = None):
# pylint: enable=bad-whitespace
    """
    Sets one or more environment variables in the image
    """

    if isinstance(key, str) and value is None:
        raise ValueError(f'Value cannot be null for {key}')
    elif not key:
        raise ValueError('Cannot add en empty set of environment variables')

    variables = {key: value} if isinstance(key, str) else key
    operation = EnvironmentOperation(variables)

    image.add_operation(operation)
