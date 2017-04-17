import click
from cookiecutter.main import cookiecutter
from manhattan.secure import random_code

from . import cli


@click.command()
def create_project():
    """Create a new manhattan project"""
    cookiecutter(
        'git@git.getme.co.uk:manhattan/manhattan_projects_cms.git',
        extra_context={
            'crsf_secret_key': random_code(32),
            'secrect_key': random_code(32)
        }
    )

cli.add_command(create_project)
