# coding=utf-8
import click
import requests

from mali_commands.tables import dict_to_csv
from .config import pass_config
from .commons import global_options, add_options, add_to_data, get_data_and_remove
from terminaltables import PorcelainTable


@click.group('projects')
def projects_commands():
    pass


@projects_commands.command('list')
@pass_config
@add_options(global_options)
def list_projects(config, **kwargs):
    from .commons import handle_api

    client_id = get_data_and_remove(kwargs, 'clientId')
    api_host = get_data_and_remove(kwargs, 'apiHost')
    auth0 = get_data_and_remove(kwargs, 'auth0')

    result = handle_api(config, requests.get, 'projects', api_host=api_host, client_id=client_id, auth0=auth0)

    format_tables = kwargs.get('output_format', 'tables') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['project_id', 'display_name', 'description', 'token', 'org']
            table_data = list(dict_to_csv(result.get('projects', []), fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)


@projects_commands.command('create')
@pass_config
@click.option('--displayName', required=True)
@click.option('--description', required=False)
@click.option('--org', required=False)
@add_options(global_options)
def create_project(config, **kwargs):
    from .commons import handle_api

    data = {}

    # noinspection SpellCheckingInspection
    add_to_data(kwargs, data, 'displayName', 'display_name')
    add_to_data(kwargs, data, 'description')
    add_to_data(kwargs, data, 'org')

    client_id = get_data_and_remove(kwargs, 'clientId')
    api_host = get_data_and_remove(kwargs, 'apiHost')
    auth0 = get_data_and_remove(kwargs, 'auth0')

    result = handle_api(config, requests.post, 'projects', data, api_host=api_host, client_id=client_id, auth0=auth0)

    format_tables = get_data_and_remove(kwargs, 'outputFormat') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['id', 'token']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)


@projects_commands.command('transfer')
@pass_config
@click.option('--projectId', required=True)
@click.option('--transferTo', required=False)
@add_options(global_options)
def transfer_project(config, **kwargs):
    from .commons import handle_api

    data = {}

    # noinspection SpellCheckingInspection
    project_id = get_data_and_remove(kwargs, 'projectid')
    # noinspection SpellCheckingInspection
    add_to_data(kwargs, data, 'transferto', 'transfer_to')

    client_id = get_data_and_remove(kwargs, 'clientId')
    api_host = get_data_and_remove(kwargs, 'apiHost')
    auth0 = get_data_and_remove(kwargs, 'auth0')

    result = handle_api(
        config, requests.post, 'projects/{project_id}/transfer'.format(project_id=project_id), data,
        api_host=api_host, client_id=client_id, auth0=auth0)

    format_tables = get_data_and_remove(kwargs, 'outputFormat') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['ok']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)
