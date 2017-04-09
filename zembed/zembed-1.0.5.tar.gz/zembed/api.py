import requests
from simplejson import JSONDecodeError
from zembed.exceptions import ZembedException


class API:
    _api_key = None
    _base_url = 'http://www.zembed.com'

    def __init__(self, api_key=''):
        self._api_key = api_key

    @classmethod
    def get_embed(cls, url, **kwargs):
        return cls._get('{}/{}'.format(cls._base_url, 'embed'), {
            'url': url, 'api_key': cls._api_key, 'format': 'json', **kwargs
        })

    @staticmethod
    def _get(url, params=None, **kwargs):
        result = requests.get(url, params=params, **kwargs)

        try:
            _response = result.json()

            if _response and 'error' in _response or result.status_code != 200:
                raise ZembedException(_response['status_code'], _response['error'], _response)

            return _response
        except JSONDecodeError:
            raise ZembedException(result.status_code, result.content.decode(), {})

    @staticmethod
    def response(response):
        return response.json()
