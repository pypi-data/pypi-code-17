# coding=utf-8
import click
import requests

from mali_commands.tables import dict_to_csv
from .config import pass_config
from .commons import global_options, add_options, add_to_data, get_data_and_remove
from terminaltables import PorcelainTable


@click.group('orgs')
def orgs_commands():
    pass


@orgs_commands.command('create')
@pass_config
@click.option('--org', required=True)
@click.option('--displayName', required=False)
@click.option('--description', required=False)
@add_options(global_options)
def create_org(config, **kwargs):
    from .commons import handle_api

    client_id = get_data_and_remove(kwargs, 'clientId')
    api_host = get_data_and_remove(kwargs, 'apiHost')
    auth0 = get_data_and_remove(kwargs, 'auth0')

    data = {}

    add_to_data(kwargs, data, 'displayName', 'display_name')
    add_to_data(kwargs, data, 'description')
    org = get_data_and_remove(kwargs, 'org')

    result = handle_api(
        config, requests.post, 'users/{org}/create'.format(org=org), data,
        api_host=api_host, client_id=client_id, auth0=auth0)

    format_tables = kwargs.get('output_format', 'tables') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['ok']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)


@orgs_commands.command('autoJoinDomain')
@pass_config
@click.option('--org', required=True)
@click.option('--domain', required=True, multiple=True)
@add_options(global_options)
def auto_join_domain(config, **kwargs):
    from .commons import handle_api

    client_id = get_data_and_remove(kwargs, 'clientId')
    api_host = get_data_and_remove(kwargs, 'apiHost')
    auth0 = get_data_and_remove(kwargs, 'auth0')

    data = {}

    add_to_data(kwargs, data, 'domain', 'domains')
    org = get_data_and_remove(kwargs, 'org')

    result = handle_api(
        config, requests.post, 'users/{org}/autoJoin'.format(org=org), data,
        api_host=api_host, client_id=client_id, auth0=auth0)

    format_tables = kwargs.get('output_format', 'tables') == 'tables'

    if result is not None:
        if format_tables:
            fields = ['ok']
            table_data = list(dict_to_csv(result, fields))

            click.echo(PorcelainTable(table_data).table)
        else:
            click.echo(result)
