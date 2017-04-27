"""
Run operation for adding shell commands to the Dockerfile
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class RunOperation(Operation):
    """
    An operation for running a shell command
    """

    commands: typing.List[str]

    def __init__(self, commands: typing.List[str]) -> None:
        """
        Creates a shell command operation
        """

        self.commands = commands if len(commands) == 1 else ['set -ex'] + commands

    def build(self) -> str:
        commands = ' \\\n    && '.join(self.commands)

        return f'RUN {commands}'
# pylint: enable=too-few-public-methods

def run(
        image,
        command: typing.Union[str, typing.List[str]]):
    """
    Adds one or more shell commands to the Docker image
    """

    if not command:
        raise ValueError('Cannot have an empty set of commands')

    operation = RunOperation(
        [command] if isinstance(command, str) else command,
    )

    image.add_operation(operation)
