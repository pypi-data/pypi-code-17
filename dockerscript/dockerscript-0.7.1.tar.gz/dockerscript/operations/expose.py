"""
Operation for exposing ports to the host or other containers
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class ExposeOperation(Operation):
    """
    Operation for exposing ports
    """

    ports: typing.List[typing.Union[int, str]]

    def __init__(self, ports: typing.List[typing.Union[int, str]]) -> None:
        """
        Creates an operation to expose ports
        """

        self.ports = ports

    def build(self) -> str:
        ports = ' '.join(
            [
                str(port)
                for port in self.ports
            ]
        )

        return f'EXPOSE {ports}'
# pylint: enable=too-few-public-methods

def expose(image, *ports: typing.Union[int, str]):
    """
    Exposes ports to the host or other containers
    """

    if not ports:
        raise ValueError('Must give at least one port to expose')

    operation = ExposeOperation(list(ports))

    image.add_operation(operation)
