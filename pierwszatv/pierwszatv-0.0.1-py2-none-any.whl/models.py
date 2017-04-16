from collections import namedtuple

BaseSourceServerStream = namedtuple(
    'BaseSourceServerStream', ['source_server', 'stream'])


class SourceServerStream(BaseSourceServerStream):

    @property
    def path(self):
        return self.stream.get_path(self.source_server.host)

    @property
    def url(self):
        return self.stream.get_url(self.source_server.host, self.stream.token)
