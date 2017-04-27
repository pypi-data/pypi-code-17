"""
Operation for setting the default Docker command
"""

import shlex

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class CommandOperation(Operation):
    """
    Operation for setting the default Docker command
    """

    command: str
    use_shell: bool

    def __init__(self, cmd: str, use_shell: bool = False) -> None:
        """
        Creates an operation to set the default command
        """

        self.command = cmd
        self.use_shell = use_shell

    def build(self) -> str:
        if self.use_shell:
            return f'CMD {self.command}'

        cmd = ', '.join(
            [
                f'"{token}"'
                for token in shlex.split(self.command)
            ]
        )

        return f'CMD [{cmd}]'
# pylint: enable=too-few-public-methods

def command(image, cmd: str, use_shell: bool = False):
    """
    Sets the default command to run when the image is run
    """

    if not cmd:
        raise ValueError('Cannot have an empty command')

    operation = CommandOperation(cmd, use_shell)

    image.add_operation(operation)
