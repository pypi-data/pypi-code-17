# coding=utf-8
import base64
import hashlib
import os
import webbrowser

import click
import requests
import sys

base_url = '_ah/api/missinglink/v1/'

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


def url_encode(d):
    try:
        from urllib.parse import urlencode
        return urlencode(d)
    except ImportError:
        import urllib
        return urllib.urlencode(d)


def urljoin(*args):
    try:
        import urlparse
        method = urlparse.urljoin
    except ImportError:
        import urllib.parse
        method = urllib.parse.urljoin

    base = args[0]
    for u in args[1:]:
        base = method(base, u)

    return base

missing_link_config = 'missinglink.cfg'


class Config(object):
    def __init__(self):
        parser = configparser.RawConfigParser()
        parser.read([missing_link_config])

        self.parser = parser

    @property
    def token_config(self):
        return self.items('token')

    @property
    def refresh_token(self):
        return self.token_config.get('refresh_token')

    @property
    def id_token(self):
        return self.token_config.get('id_token')

    def items(self, section=None):
        try:
            return dict(self.parser.items(section))
        except configparser.NoSectionError:
            return {}

    def set(self, section, key, val):
        try:
            self.parser.add_section(section)
        except configparser.DuplicateSectionError:
            pass

        self.parser.set(section, key, val)

    def write(self, fo):
        self.parser.write(fo)


pass_config = click.make_pass_decorator(Config, ensure=True)


global_options = [
    click.option('--api_host', default='https://missinglink.appspot.com', required=False),
    click.option('--host', default='https://missinglink.ai', required=False),
    click.option('--client_id', default='nbkyPAMoxj5tNzpP07vyrrsVZnhKYhMj', required=False),
    click.option('--auth0', default='missinglink', required=False)
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


# noinspection PyUnusedLocal
@click.group()
def cli(**kwargs):
    pass


@click.group('auth')
def auth_commands():
    pass


def auth0_url(auth0):
    return '{}.auth0.com'.format(auth0)


def update_token(client_id, config, auth0):
    r = requests.post('https://{}/delegation'.format(auth0_url(auth0)), json={
        'client_id': client_id,
        'grant_type': "urn:ietf:params:oauth:grant-type:jwt-bearer",
        'refresh_token': config.refresh_token,
    })

    r.raise_for_status()

    data = r.json()

    config.set('token', 'id_token', data['id_token'])

    with open(missing_link_config, 'w') as configfile:
        config.write(configfile)


def pixy_flow(client_id, host, auth0, **kwargs):
    verifier = base64url(os.urandom(32))
    verifier_challenge = base64url(sha256(verifier))

    verifier = verifier.decode('ascii')
    verifier_challenge = verifier_challenge.decode('ascii')

    query = {
        'response_type': 'code',
        'scope': 'openid offline_access user_external_id',
        'client_id': client_id,
        'redirect_uri': host + '/admin/auth/init',
        'code_challenge': verifier_challenge,
        'code_challenge_method': 'S256'
    }

    authorize_url = 'https://{}/authorize?{}'.format(auth0_url(auth0), url_encode(query))

    print("If the browser doesn't open enter this URL manually\n%s\n" % authorize_url)

    webbrowser.open(authorize_url)

    if sys.version_info >= (3, 0):
        code = input('Enter the token ')
    else:
        # noinspection PyUnresolvedReferences
        code = raw_input('Enter the token ')

    r = requests.post('https://{}/oauth/token'.format(auth0_url(auth0)), json={
        'code': code,
        'code_verifier': verifier,
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'redirect_uri': host + '/admin/auth/success',
    })

    r.raise_for_status()

    data = r.json()

    print("Success!, you sre authorized to use the command line.")

    return data['access_token'], data['refresh_token'], data['id_token']


@auth_commands.command('init')
@click.pass_context
@pass_config
@add_options(global_options)
def init_auth(config, **kwargs):
    access_token, refresh_token, id_token = pixy_flow(**kwargs)

    config.set('token', 'access_token', access_token)
    config.set('token', 'refresh_token', refresh_token)
    config.set('token', 'id_token', id_token)

    with open(missing_link_config, 'w') as configfile:
        config.write(configfile)


@click.group('projects')
def projects_commands():
    pass


def base64url(b):
    return bytearray(base64.b64encode(b).decode('ascii').replace('=', '').replace('+', '-').replace('/', '_'), 'ascii')


def sha256(s):
    h = hashlib.sha256()
    h.update(s)
    return h.digest()


def handle_api(config, http_method, method_url, data=None, client_id=None, api_host=None, auth0=None, **kwargs):
    url = urljoin(api_host, base_url, method_url)

    for retries in range(3):
        headers = {'Authorization': 'Bearer {}'.format(config.id_token)}
        r = http_method(url, headers=headers, json=data)

        if r.status_code == 401:
            update_token(client_id, config, auth0)
            continue

    r.raise_for_status()

    return r.json()


@projects_commands.command('list')
@pass_config
@add_options(global_options)
def list_projects(config, **kwargs):
    return handle_api(config, requests.get, 'projects', **kwargs)


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

    return handle_api(config, requests.post, 'projects', data, **kwargs)


cli.add_command(auth_commands)
cli.add_command(projects_commands)

if __name__ == "__main__":
    cli()
