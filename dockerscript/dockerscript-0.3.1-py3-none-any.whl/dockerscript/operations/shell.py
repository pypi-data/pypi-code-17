"""
Operation for setting the shell of the image
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class ShellOperation(Operation):
    """
    Operation that sets the shell of the image
    """

    shell: str
    arguments: typing.List[str]

    def __init__(self, command_shell: str, arguments: typing.List[str]):
        """
        Creates an operation to set the image shell
        """

        self.shell = command_shell
        self.arguments = arguments

    def build(self) -> str:
        command = ', '.join(
            [
                f'"{arg}"'
                for arg in [self.shell] + self.arguments
            ]
        )

        return f'SHELL [{command}]'
# pylint: enable=too-few-public-methods

def shell(image, command_shell: str, *args: typing.List[str]):
    """
    Sets the shell of the image
    """

    operation = ShellOperation(command_shell, args)

    image.add_operation(operation)
