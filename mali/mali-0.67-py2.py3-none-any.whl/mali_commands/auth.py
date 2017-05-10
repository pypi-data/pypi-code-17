# coding=utf-8
import click
from .commons import add_options, global_options, get_data_and_remove
from .config import pass_config


@click.group('auth')
def auth_commands():
    pass


@auth_commands.command('init')
@click.pass_context
@pass_config
@add_options(global_options)
def init_auth(config, **kwargs):
    from .commons import pixy_flow

    client_id = get_data_and_remove(kwargs, 'clientId')
    host = get_data_and_remove(kwargs, 'host')
    auth0 = get_data_and_remove(kwargs, 'auth0')

    access_token, refresh_token, id_token = pixy_flow(client_id=client_id, host=host, auth0=auth0)

    config.update_and_save({
        'token': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'id_token': id_token,
        }
    })
