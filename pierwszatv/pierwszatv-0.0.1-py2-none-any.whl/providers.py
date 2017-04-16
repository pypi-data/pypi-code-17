from pierwszatv.api.providers import SourceServersProvider
from pierwszatv.socket.clients import PierwszaTvSocket
from pierwszatv.socket.providers import StreamProvider
from pierwszatv.models import SourceServerStream


class PierwszaTvStreamProvider(object):

    def __init__(self, streaming_api):
        self.streaming_api = streaming_api

    def provide(self, source_id):
        source_servers_provider = self._get_source_servers_provider()
        source_servers_iter = source_servers_provider.provide(source_id)

        for source_server in source_servers_iter:
            stream_id = self.streaming_api.request_stream(
                source_id, source_server.id, source_server.token)

            stream_provider = self._get_stream_provider(source_server.host)
            stream = stream_provider.provide(source_server.token, stream_id)
            yield SourceServerStream(source_server, stream)

    def _get_source_servers_provider(self):
        return SourceServersProvider(self.streaming_api)

    def _get_streaming_socket(self, server_host):
        return PierwszaTvSocket(server_host, 8004)

    def _get_stream_provider(self, server_host):
        socket = self._get_streaming_socket(server_host)
        return StreamProvider(socket)
