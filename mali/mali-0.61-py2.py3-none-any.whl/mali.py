# coding=utf-8
import click
from mali_commands import auth_commands, projects_commands


# noinspection PyUnusedLocal
@click.group()
def cli(**kwargs):
    pass


cli.add_command(auth_commands)
cli.add_command(projects_commands)

if __name__ == "__main__":
    cli()
