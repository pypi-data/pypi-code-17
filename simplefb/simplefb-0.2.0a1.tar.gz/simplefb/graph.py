import json
import urllib.parse
import urllib.request

import aiohttp

FB_API_HOST = 'https://graph.facebook.com'


def fb_exchange_token(app_id, app_secret, short_lived_token):
    endpoint = '/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token,
    }
    return urllib.parse.parse_qs(
        _api(endpoint, 'GET', params)
    )


def me(access_token, fields=('id', 'name')):
    return api(
        '/me', 'GET', {
            'access_token': access_token,
            'fields': ','.join(fields)
        }
    )


def api(endpoint, method, params, data=None):
    return json.loads(_api(endpoint, method, params, data))


def _api(endpoint, method, params, data=None):
    url_params = urllib.parse.urlencode(params)
    url = '{}{}?{}'.format(FB_API_HOST, endpoint, url_params)
    request = urllib.request.Request(url=url, data=data, method=method)
    return urllib.request.urlopen(request).read().decode('utf-8')


async def fb_exchange_token_async(app_id,
                                  app_secret,
                                  short_lived_token):
    endpoint = '/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token,
    }
    return urllib.parse.parse_qs(
        await _api_async(endpoint, 'GET', params)
    )


async def me_async(access_token, fields=('id', 'name')):
    return await api_async(
        '/me', 'GET', {
            'access_token': access_token,
            'fields': ','.join(fields)
        }
    )


async def api_async(endpoint, method, params, data=None):
    return json.loads(await _api_async(endpoint, method, params, data))


async def _api_async(endpoint, method, params, data=None):
    url_params = urllib.parse.urlencode(params)
    url = '{}{}?{}'.format(FB_API_HOST, endpoint, url_params)
    data = None if data is None else json.dumps(data)
    async with aiohttp.ClientSession() as session:
        response = getattr(session, method.lower())(url, data=data)
        return await response.text(encoding='utf-8')
