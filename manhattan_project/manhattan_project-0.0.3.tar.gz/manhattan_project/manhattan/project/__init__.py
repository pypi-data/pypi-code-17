import click

__all__ = ['cli']


@click.group()
def cli():
    """
    Basic entry point for manhattan project scripts `manhattan {command} ...`
    """
    pass


# Import commands

from . import blueprints
from . import projects
