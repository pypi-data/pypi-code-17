import requests

from eva.conf import settings
from eva.utils.dict import dict_to_namedtuple


class API(object):

    def __init__(self, url_prefix=None, sid=None):
        if not url_prefix:
            url_prefix = settings.API_URL_PREFIX

        if url_prefix.endswith('/'):
            url_prefix = url_prefix[:-1]

        self.url_prefix = url_prefix
        self.sid = sid

        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
            if self.sid:
                self._session.headers.update({
                    'Authorization': 'OOC {0}'.format(self.sid)
                })
        return self._session

    def full_url(self, path):
        return self.url_prefix + path

    def request(self, method, path, **kwargs):
        url = self.full_url(path)
        r = self.session.request(method, url, **kwargs)
        if 'Content-Type' in r.headers and 'application/json' in r.headers['Content-Type']:
            return dict_to_namedtuple(r.json())
        return r.text

    def raw_request(self, method, path, **kwargs):
        url = self.full_url(path)
        r = self.session.request(method, url, **kwargs)
        if 'Content-Type' in r.headers and 'application/json' in r.headers['Content-Type']:
            return r.json()
        return r.text

    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('DELETE', path, **kwargs)
