from collections import namedtuple

from six.moves.urllib.parse import urlencode

from pierwszatv.urls import parse_url

BaseLive = namedtuple('BaseLive', ['status', 'token', 'url'])
BaseStreamSource = namedtuple(
    'BaseStreamSource', ['source', 'sourceError', 'started', 'status'])
BaseSourceServer = namedtuple('BaseSourceServer', ['token', 'id', 'server'])


class Live(BaseLive):
    pass


class StreamSource(BaseStreamSource):

    def get_url(self, stream_token):
        query = urlencode({'token': stream_token})
        return '?'.join([self.source, query])


class SourceServer(BaseSourceServer):

    @property
    def host(self):
        server_host, server_port = parse_url(self.server)
        return server_host
