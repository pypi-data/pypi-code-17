"""
Base operation implementation
"""

import abc
import typing

# pylint: disable=too-few-public-methods
class Operation(metaclass=abc.ABCMeta):
    """
    Base operation implementation
    """

    @abc.abstractmethod
    def build(self) -> str:
        """
        Builds the final operation that will appear in the Dockerfile
        """

    def __eq__(self, op: typing.Any) -> bool:
        return isinstance(op, self.__class__) and self.__dict__ == op.__dict__

    def __hash__(self) -> int:
        data = self.__dict__

        keys = sorted(data.keys())

        return hash(data[key] for key in keys)
# pylint: enable=too-few-public-methods
