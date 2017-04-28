"""
Label operation
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class LabelOperation(Operation):
    """
    Operation that adds labelled data to a Dockerfile
    """

    labels: typing.Dict[str, typing.Any]

    def __init__(self, labels: typing.Dict[str, typing.Any]) -> None:
        self.labels = labels

    def build(self) -> str:
        data = ' \\\n      '.join(
            [
                f'"{key}"="{value}"'
                for key, value in self.labels.items()
            ]
        )

        return f'LABEL {data}'
# pylint: enable=too-few-public-methods

# pylint: disable=bad-whitespace
def label(
        image,
        key: typing.Union[str, typing.Dict[str, typing.Any]],
        value: typing.Union[None, typing.Any] = None):
# pylint: enable=bad-whitespace
    """
    Adds labelled data to the Docker image
    """

    if isinstance(key, str) and value is None:
        raise ValueError(f'Non-null value must be given for key: {key}')

    labels = {key: value} if isinstance(key, str) else key
    if not labels:
        raise ValueError('Cannot have an empty set of labels')

    operation = LabelOperation(labels)

    image.add_operation(operation)
