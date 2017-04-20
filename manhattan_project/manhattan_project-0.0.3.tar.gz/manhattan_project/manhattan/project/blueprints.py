import click
from cookiecutter.main import cookiecutter

from . import cli


@click.command('create-blueprint')
def create_blueprint():
    """Create a new manhattan project"""
    cookiecutter(
        'git@git.getme.co.uk:manhattan/manhattan_blueprints_base.git'
    )

cli.add_command(create_blueprint)
