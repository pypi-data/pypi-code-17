from pierwszatv.socket.models import Stream


class StreamProvider(object):

    def __init__(self, streaming_socket):
        self.streaming_socket = streaming_socket

    def provide(self, source_server_token, stream_id):
        stream_token = self.streaming_socket.authorize(source_server_token)
        stream_data = self.streaming_socket.subscribe(stream_id)
        return Stream(stream_token, **stream_data)
