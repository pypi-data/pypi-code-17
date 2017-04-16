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

__version__ = '0.3'

import click
import json
import webbrowser

try:
    from http.server import HTTPServer
    from http.server import BaseHTTPRequestHandler
except ImportError:
    # Fallback to Python 2
    from BaseHTTPServer import HTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler

from .config import CONFIG


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Withings-cli: you may close this tab.'.encode())
        self.oauth.parse_authorization_response(self.path)

    def log_message(self, format, *args):
        return  # Silence log messages


@click.group()
def cli():
    pass


@cli.command()
@click.argument('option', type=str)
@click.argument('value', type=str)
def config(option, value):
    """Configure Withings API key and secret.

    For example, 'withings config apikey 77..cf379b'
    """
    CONFIG[option] = value


@cli.command()
@click.argument('user')
def add(user):
    """Authorize to access user information."""
    from requests_oauthlib import OAuth1Session
    from .config import WITHINGS_OAUTH_URI, CALLBACK_URI

    try:
        oauth = OAuth1Session(
            CONFIG['apikey'],
            CONFIG['apisecret'],
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
    CONFIG['users'][user] = tokens
    click.echo('User \'{}\' has been added.'.format(user))


@cli.command()
def list():
    """Prints user list."""
    for user in CONFIG['users'].keys():
        click.echo(user)


@cli.command()
@click.argument('user')
@click.option('--version', '-v', type=int, help='Withings API version.')
@click.option('--service', '-s', type=str, help='Withings API service.')
@click.option('--param', '-p', type=(str, str), multiple=True, help='Withings API service parameters.')
@click.option('--pp', is_flag=True, help='Pretty print query result.')
@click.option('--debug', is_flag=True, help='Show query URI.')
def query(user, version, service, param, pp, debug):
    """Runs API query for a given user.

    For example, 'withings query -s measure -p action getmeas me', would fetch
    body measures for user 'me'.
    """
    from sys import stderr
    from requests_oauthlib import OAuth1Session
    from .config import WITHINGS_API_URI

    if version is 2:
        uri = WITHINGS_API_URI + '/v2'
    else:
        uri = WITHINGS_API_URI
    uri += '/{}'.format(service)

    try:
        user = CONFIG['users'][user]
    except KeyError:
        click.echo('Unknown user \'{}\'.'.format(user))
        raise click.Abort()

    params = dict(param)
    params['userid'] = user['userid']

    oauth = OAuth1Session(
        CONFIG['apikey'],
        CONFIG['apisecret'],
        resource_owner_key=user['oauth_token'],
        resource_owner_secret=user['oauth_token_secret'],
        signature_type='query'
    )

    r = oauth.get(uri, params=params)
    content = json.loads(r.content.decode())

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
