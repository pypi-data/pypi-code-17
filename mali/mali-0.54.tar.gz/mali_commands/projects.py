# coding=utf-8
import click
import requests

from mali_commands.tables import dict_to_csv
from .config import pass_config
from .commons import handle_api, global_options, add_options
from terminaltables import PorcelainTable


@click.group('projects')
def projects_commands():
    pass


@projects_commands.command('list')
@pass_config
@add_options(global_options)
def list_projects(config, **kwargs):
    result = handle_api(config, requests.get, 'projects', **kwargs)

    format_tables = kwargs.get('output_format', 'tables') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['project_id', 'display_name', 'description', 'token']
            table_data = list(dict_to_csv(result.get('projects', []), fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)


@projects_commands.command('create')
@pass_config
@click.option('--displayName', required=True)
@click.option('--description', required=False)
@add_options(global_options)
def create_project(config, **kwargs):
    # noinspection SpellCheckingInspection
    data = {
        'display_name': kwargs.get('displayname'),
        'description': kwargs.get('description')
    }

    result = handle_api(config, requests.post, 'projects', data, **kwargs)

    format_tables = kwargs.get('output_format', 'tables') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['id', 'token']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)
