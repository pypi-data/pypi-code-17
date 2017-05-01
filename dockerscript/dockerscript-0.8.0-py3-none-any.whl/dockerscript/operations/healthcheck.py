"""
Operation for setting the healthcheck of a Docker image
"""

import typing

from .base_operation import Operation

# pylint: disable=too-few-public-methods
class HealthcheckOperation(Operation):
    """
    Operation for setting the healthcheck of a Docker image
    """

    command: str
    interval: typing.Union[str, None]
    timeout: typing.Union[str, None]
    retries: typing.Union[int, None]

    # pylint: disable=bad-whitespace
    def __init__(
            self,
            command: str,
            interval: typing.Union[str, None] = None,
            timeout: typing.Union[str, None] = None,
            retries: typing.Union[int, None] = None) -> None:
    # pylint: enable=bad-whitespace
        """
        Creates the healthcheck operation
        """

        self.command = command
        self.interval = interval
        self.timeout = timeout
        self.retries = retries

    def build(self) -> str:
        options = ' '.join(
            [
                f'--{name}={value}'
                for name, value in self.__dict__.items()
                if name != 'command' and value is not None
            ]
        )

        return f'HEALTHCHECK {options} CMD {self.command}'
# pylint: enable=too-few-public-methods

# pylint: disable=bad-whitespace
def healthcheck(
        image,
        command: str,
        interval: typing.Union[str, None] = None,
        timeout: typing.Union[str, None] = None,
        retries: typing.Union[int, None] = None):
# pylint: enable=bad-whitespace
    """
    Sets the healthcheck operation
    """

    if not command:
        raise ValueError('Command is required for healthcheck')

    operation = HealthcheckOperation(
        command,
        interval=interval,
        timeout=timeout,
        retries=retries,
    )

    image.add_operation(operation)
