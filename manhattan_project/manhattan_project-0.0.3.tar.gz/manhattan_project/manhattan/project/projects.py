import click
from cookiecutter.main import cookiecutter
from manhattan.secure import random_code

from . import cli


@click.command('create-project')
def create_project():
    """Create a new manhattan project"""
    cookiecutter(
        'git@git.getme.co.uk:manhattan/manhattan_projects_cms.git',
        extra_context={
            'csrf_secret_key': random_code(32),
            'secret_key': random_code(32)
        }
    )

cli.add_command(create_project)
