from pierwszatv.api.models import SourceServer


class SourceServersProvider(object):

    def __init__(self, streaming_api):
        self.streaming_api = streaming_api

    def provide(self, source_id):
        source_servers_data = self.streaming_api.get_play(source_id)
        for source_server_data in source_servers_data:
            yield SourceServer(**source_server_data)
