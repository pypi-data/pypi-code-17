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
        **variables: typing.Any):
# pylint: enable=bad-whitespace
    """
    Sets one or more environment variables in the image
    """

    if not variables:
        raise ValueError('Must give at least one environment variable')

    operation = EnvironmentOperation(variables)

    image.add_operation(operation)
