import requests

from six.moves.urllib.parse import urljoin

from pierwszatv.api.exceptions import PierwszaTvApiError
from pierwszatv.api.models import Live, StreamSource


class PierwszaTvApi(object):

    BASE_URL = 'http://pierwsza.tv/api/'
    API_ID = 'W4ER'
    CHECKSUM = 'a4d425e463160798c7aab988a67c1218'

    def get_base_url(self):
        return self.BASE_URL

    def request(self, path, params=None):
        base_url = self.get_base_url()
        url = urljoin(base_url, path)

        if params is None:
            params = {}

        resp = requests.get(url, params=params)
        data = resp.json()

        if 'status' not in data or data['status'] != 'ok':
            raise PierwszaTvApiError(data['message'])

        return data

    def get_channels(self):
        path = 'channels'
        params = {
            'api_id': self.API_ID,
            'checksum': self.CHECKSUM,
        }
        result = self.request(path, params=params)
        return result['channels']

    def get_stream_source(self, server_id, stream_id):
        path = 'stream/status'
        params = {
            'api_id': self.API_ID,
            'checksum': self.CHECKSUM,
            'serverId': server_id,
            'streamId': stream_id,
        }
        result = self.request(path, params=params)
        return StreamSource(**result)

    def refresh_stream(self, stream_id, server_id, token):
        path = 'stream/refresh'
        params = {
            'api_id': self.API_ID,
            'checksum': self.CHECKSUM,
            'serverId': server_id,
            'streamId': stream_id,
            'token': token,
        }
        result = self.request(path, params=params)
        return result


class PierwszaTvStreamingApi(object):

    SCHEME = 'http'
    NETLOC = '91.240.87.72:8875'

    def request(self, path, params=None):
        base_url = self.get_base_url()
        url = urljoin(base_url, path)

        if params is None:
            params = {}

        resp = requests.get(url, params=params)
        data = resp.json()

        if 'status' not in data or not data['status']:
            raise PierwszaTvApiError

        return data

    def get_base_url(self):
        return '://'.join([self.SCHEME, self.NETLOC])

    def get_live(self):
        path = '/live'
        params = {'wt': ''}
        return self.request(path, params=params)

    def get_sources(self):
        path = '/sources'
        params = {'watchToken': ''}
        result = self.request(path, params=params)
        return result['sources']

    def get_playlists(self):
        path = '/playlists'
        params = {'watchToken': ''}
        result = self.request(path, params=params)
        return result['playlists']

    def get_play(self, source_id):
        path = '/play'
        params = {
            'id': source_id,
            'watchToken': '',
        }
        result = self.request(path, params=params)
        return result['servers']

    def request_stream(self, source_id, server_id, token):
        cs = '1933092e34c38c81f40cbdf0bdd69b49a33313f906ab604dac028784671dbeac'
        path = '/request-stream'
        params = {
            'token': token,
            'server': server_id,
            'source': source_id,
            'cs': cs,
        }
        result = self.request(path, params=params)
        return result['id']


class PierwszaTvPlayer(object):

    BASE_URL = 'http://pierwsza.tv/player/'

    def get_base_url(self):
        return self.BASE_URL

    def request(self, path, params=None):
        base_url = self.get_base_url()
        url = urljoin(base_url, path)

        if params is None:
            params = {}

        return requests.get(url, params=params)

    def report_ok(self, source_id, server_id, stream_id):
        path = 'report-ok'
        params = {
            'id': source_id,
            'serverId': server_id,
            'streamId': stream_id,
        }
        resp = self.request(path, params=params)

        return resp.status_code == 200
