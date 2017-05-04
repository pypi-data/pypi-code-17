# coding=utf-8
import base64
import hashlib
import os
import webbrowser

import click
import requests
import sys

from .config import missing_link_config

base_url = '_ah/api/missinglink/v1/'


def auth0_url(auth0):
    return '{}.auth0.com'.format(auth0)


global_options = [
    click.option('--apiHost', default='https://missinglinkai.appspot.com', required=False),
    click.option('--host', default='https://missinglink.ai', required=False),
    click.option('--clientId', default='nbkyPAMoxj5tNzpP07vyrrsVZnhKYhMj', required=False),
    click.option('--auth0', default='missinglink', required=False),
    click.option('--outputFormat', '-o', type=click.Choice(['tables', 'json']), default='tables', required=False)
]


def add_to_data(kwargs, data, key, data_key=None):
    key = key.lower()

    if kwargs.get(key) is not None:
        data[data_key if data_key else key] = kwargs[key]

    if key in kwargs:
        del kwargs[key]


def get_data_and_remove(kwargs, key):
    key = key.lower()
    result = kwargs.get(key)

    if key in kwargs:
        del kwargs[key]

    return result

def base64url(b):
    return bytearray(base64.b64encode(b).decode('ascii').replace('=', '').replace('+', '-').replace('/', '_'), 'ascii')


def sha256(s):
    h = hashlib.sha256()
    h.update(s)
    return h.digest()


def url_encode(d):
    try:
        # noinspection PyUnresolvedReferences
        from urllib.parse import urlencode
        return urlencode(d)
    except ImportError:
        import urllib
        # noinspection PyUnresolvedReferences
        return urllib.urlencode(d)


def urljoin(*args):
    try:
        # noinspection PyUnresolvedReferences
        import urlparse
        method = urlparse.urljoin
    except ImportError:
        import urllib.parse
        method = urllib.parse.urljoin

    base = args[0]
    for u in args[1:]:
        base = method(base, u)

    return base


# noinspection PyUnusedLocal
def handle_api(config, http_method, method_url, data=None, client_id=None, api_host=None, auth0=None):
    url = urljoin(api_host, base_url, method_url)

    result = None
    for retries in range(3):
        headers = {'Authorization': 'Bearer {}'.format(config.id_token)}
        r = http_method(url, headers=headers, json=data)

        if r.status_code == 401:
            update_token(client_id, config, auth0)
            continue

        r.raise_for_status()
        result = r.json()
        break

    if result is None:
        click.echo('failed to refresh the token, rerun auth init again', err=True)

    return result


def update_token(client_id, config, auth0):
    r = requests.post('https://{}/delegation'.format(auth0_url(auth0)), json={
        'client_id': client_id,
        'grant_type': "urn:ietf:params:oauth:grant-type:jwt-bearer",
        'scope': 'openid offline_access user_external_id',
        'refresh_token': config.refresh_token,
    })

    r.raise_for_status()

    data = r.json()

    config.set('token', 'id_token', data['id_token'])

    with open(missing_link_config, 'w') as configfile:
        config.write(configfile)


# noinspection PyUnusedLocal
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


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options
