"""
Operation for setting the default Docker command
"""

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class CommandOperation(Operation):
    """
    Operation for setting the default Docker command
    """

    command: str

    def __init__(self, cmd: str) -> None:
        """
        Creates an operation to set the default command
        """

        self.command = cmd

    def build(self) -> str:
        return f'CMD {self.command}'
# pylint: enable=too-few-public-methods

def command(image, cmd: str):
    """
    Sets the default command to run when the image is run
    """

    if not cmd:
        raise ValueError('Cannot have an empty command')

    operation = CommandOperation(cmd)

    image.add_operation(operation)
