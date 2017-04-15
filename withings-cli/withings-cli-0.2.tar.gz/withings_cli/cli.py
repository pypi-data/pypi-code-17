"""
MIT License

Copyright (c) 2017 Kim Blomqvist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import click
import pytoml as toml
import json
import webbrowser
import collections

from os import path
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

__version__ = '0.2'

CONFIG_FILE = path.join(path.expanduser("~"), '.withings')
CONFIG_OPTIONS = ('apikey', 'apisecret')

CALLBACK_URI = ('localhost', 1337)
WITHINGS_API_URI = 'https://wbsapi.withings.net'
WITHINGS_OAUTH_URI = 'https://oauth.withings.com/account'

class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("Withings-cli: you may close this tab.")
        self.oauth.parse_authorization_response(self.path)

    def log_message(self, format, *args):
        return


def load_configs():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return toml.load(file)
    except EnvironmentError:
        return dict()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('opt', type=str)
@click.argument('value', type=str)
def config(opt, value):
    """Configure Withings API key and secret.

    For example, 'withings config apikey 77..cf379b'
    """
    if opt not in CONFIG_OPTIONS:
        click.echo("Invalid config: Not in {}".format(CONFIG_OPTIONS))
        raise click.Abort()

    configs = load_configs()
    configs[opt] = value
    with open(CONFIG_FILE, 'w') as file:
        toml.dump(configs, file)
    
    from os import chmod
    chmod(CONFIG_FILE, 0o600)


@cli.command()
@click.argument('user')
def add(user):
    """Authorize to access user information."""
    from requests_oauthlib import OAuth1Session
    configs = load_configs()

    try:
        oauth = OAuth1Session(
            configs['apikey'],
            configs['apisecret'],
            callback_uri='http://{}:{}'.format(*CALLBACK_URI)
        )
    except KeyError:
        click.echo('Oops... missing Withings client key and secret')
        raise click.Abort()

    oauth.fetch_request_token(WITHINGS_OAUTH_URI + '/request_token')
    url = oauth.authorization_url(WITHINGS_OAUTH_URI + '/authorize')

    click.echo('Authorize withings-cli to access user information.')
    webbrowser.open_new_tab(url)

    CallbackHandler.oauth = oauth
    httpd = HTTPServer(CALLBACK_URI, CallbackHandler)
    httpd.handle_request()

    tokens = oauth.fetch_access_token(WITHINGS_OAUTH_URI + '/access_token')

    if not 'users' in configs:
        configs['users'] = dict()
    configs['users'][user] = tokens
    with open(CONFIG_FILE, 'w') as file:
        toml.dump(configs, file)

    click.echo('User \'{}\' has been added.'.format(user))


@cli.command()
def list():
    """Prints user list."""
    configs = load_configs()
    try:
        for user in configs['users'].keys():
            click.echo(user)
    except KeyError:
        pass


@cli.command()
@click.argument('user')
@click.option('--version', '-v', type=int, help='Withings API version.')
@click.option('--service', '-s', type=str, help='Withings API service.')
@click.option('--param', '-p', type=(str, str), multiple=True, help='Withings API service parameters.')
@click.option('--pp', is_flag=True, help='Pretty print results.')
@click.option('--debug', is_flag=True, help='Show request URI')
def query(user, version, service, param, pp, debug):
    """Runs API query for a given user.

    For example, 'withings query -s measure -p action getmeas me', would fetch
    body measures for user 'me'.
    """
    from sys import stderr
    from requests_oauthlib import OAuth1Session

    if version is 2:
        uri = WITHINGS_API_URI + '/v2'
    else:
        uri = WITHINGS_API_URI
    uri += "/{}".format(service)

    configs = load_configs()
    user = configs['users'][user]

    params = dict(param)
    params['userid'] = user['userid']

    oauth = OAuth1Session(
        configs['apikey'],
        configs['apisecret'],
        resource_owner_key=user['oauth_token'],
        resource_owner_secret=user['oauth_token_secret'],
        signature_type='query'
    )

    r = oauth.get(uri, params=params)
    content = json.loads(r.content)

    if debug:
        click.echo(r.url, file=stderr)
    if content['status'] != 0:
        click.echo(r.content, file=stderr)
        raise click.Abort()

    if not pp:
        click.echo(content.get('body'))
    else:
        from pprint import PrettyPrinter
        pp = PrettyPrinter(indent=2, width=72)
        pp.pprint(content.get('body'))


@cli.command()
@click.pass_context
@click.argument('user')
@click.option('--pp', is_flag=True, help='Pretty print results.')
def whois(ctx, user, pp):
    """Prints user info."""
    query_params = {
        'version': 1,
        'user': user,
        'service': 'user',
        'param': (('action', 'getbyuserid'),),
        'pp': pp
    }
    ctx.invoke(query, **query_params)


if __name__ == '__main__':
    cli()
