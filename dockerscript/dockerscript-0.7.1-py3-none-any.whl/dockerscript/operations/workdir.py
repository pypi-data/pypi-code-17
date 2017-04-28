"""
Operation for setting the working directory of an image
"""

import pathlib
import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class WorkdirOperation(Operation):
    """
    Operation for setting the working directory of an image
    """

    path: pathlib.Path

    def __init__(self, path: pathlib.Path) -> None:
        """
        Creates an operation to set the image to the given directory
        """

        self.path = path

    def build(self) -> str:
        return f'WORKDIR {self.path}'
# pylint: enable=too-few-public-methods

def workdir(image, directory: typing.Union[str, pathlib.Path]):
    """
    Sets the working directory of the image
    """

    directory_path = directory if isinstance(directory, pathlib.Path) else pathlib.Path(directory)
    operation = WorkdirOperation(directory_path)

    image.add_operation(operation)
