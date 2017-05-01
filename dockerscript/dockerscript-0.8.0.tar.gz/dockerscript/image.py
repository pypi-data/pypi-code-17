"""
Class for managing Dockerfiles
"""

import pathlib
import typing

import colored

import dockerscript.operations

class Image:
    """
    Data structure for mapping out a Dockerfile
    """

    operations: typing.List[dockerscript.operations.Operation]

    # pylint: disable=bad-whitespace
    def __init__(self, filename: typing.Union[str, pathlib.Path] = 'Dockerfile') -> None:
    # pylint: enable=bad-whitespace
        """
        Creates an image instance that can write to the given path
        """

        self.filename = filename if filename is pathlib.Path else pathlib.Path(filename)
        self.operations = []

    def add_operation(self, operation: dockerscript.operations.Operation):
        """
        Adds an operation to the image
        """

        if operation is None:
            raise ValueError('Operation cannot be None')

        self.operations.append(operation)

    def build(self):
        """
        Generates a Dockerfile
        """

        if not self.operations:
            print(colored.stylize('No operations defined', colored.fg('yellow')))
            return

        with open(self.filename, 'w') as dockerfile:
            for operation in self. operations:
                dockerfile.write(f'{operation.build()}\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.build()

        return self
