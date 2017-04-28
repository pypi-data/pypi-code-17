"""
Operation for copying files into the Docker image
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class CopyOperation(Operation):
    """
    Operation for copying files into the Docker image
    """

    sources: typing.List[str]
    destination: str

    def __init__(self, sources: typing.List[str], destination: str) -> None:
        """
        Creates an operation to copy files into the image
        """

        self.sources = sources
        self.destination = destination

    def build(self) -> str:
        sources = ', '.join(
            [
                f'"{src}"'
                for src in self.sources
            ]
        )

        return f'COPY [{sources}, "{self.destination}"]'
# pylint: enable=too-few-public-methods

def copy(image, *paths: str):
    """
    Copies files into the Docker image
    """

    path_count = len(paths)
    if path_count == 0:
        raise ValueError('No source files were given')
    elif path_count == 1:
        raise ValueError('No destination path was given')

    sources = list(paths[:-1])
    destination = paths[-1]

    operation = CopyOperation(sources, destination)

    image.add_operation(operation)
