"""
Operation for setting a Dockerfile's current image
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class BaseImageOperation(Operation):
    """
    Operation that sets the Dockerfile's current image
    """

    name: str
    tag: typing.Union[str, None]
    digest: typing.Union[str, None]

    # pylint: disable=bad-whitespace
    def __init__(
            self,
            name: str,
            tag: typing.Union[str, None] = None,
            digest: typing.Union[str, None] = None) -> None:
    # pylint: enable=bad-whitespace
        """
        Creates a new base image operation with the given image and tag
        """

        self.name = name
        self.tag = tag
        self.digest = digest

    def build(self) -> str:
        if self.tag is not None:
            image = f'{self.name}:{self.tag}'
        elif self.digest is not None:
            image = f'{self.name}@{self.digest}'
        else:
            image = self.name

        return f'FROM {image}'
# pylint: enable=too-few-public-methods

# pylint: disable=bad-whitespace
def base_image(
        image,
        name: str,
        tag: typing.Union[str, None] = None,
        digest: typing.Union[str, None] = None):
# pylint: enable=bad-whitespace
    """
    Sets the Dockerfile's current base image
    """

    if tag is not None and digest is not None:
        raise ValueError('Cannot define both tag and digest on Docker image')

    operation = BaseImageOperation(name, tag, digest)

    image.add_operation(operation)
