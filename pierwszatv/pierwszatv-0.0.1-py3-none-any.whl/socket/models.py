from collections import namedtuple

from six.moves.urllib.parse import urljoin, urlencode

BaseStream = namedtuple(
    'BaseStream', ['id', 'error', 'url', 'started', 'pid', 'port'])


class Stream(BaseStream):

    SCHEME = 'http'

    def __new__(cls, token, **data):
        new = BaseStream.__new__(cls, **data)
        new.token = token
        return new

    def get_base_url(self, server_host):
        return '{0}://{1}:{2}'.format(self.SCHEME, server_host, self.port)

    def get_path(self, server_host):
        base_url = self.get_base_url(server_host)
        return urljoin(base_url, self.url)

    def get_url(self, server_host, stream_token):
        full_path = self.get_path(server_host)
        query = urlencode({'token': stream_token})
        return '?'.join([full_path, query])
