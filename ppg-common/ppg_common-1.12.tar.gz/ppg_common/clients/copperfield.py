from ppg_common.clients.base import BaseClient


class CopperfieldClient(BaseClient):
    urls = {
        "execute": "/v1/operations/execute/{}",
        "status": "/v1/operations/status/{}",
        "abort": "/v1/operations/abort/{}"
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(CopperfieldClient, self).__init__(host, port, ssl, session)

    def show_status(self, file_id):
        return self.get(self.urls.get('status').format(file_id))

    def abort_task(self, file_id):
        return self.get(self.urls.get('abort').format(file_id))

    def execute(self, box, input_file, command, output_file):
        body = {
            'input_file': input_file,
            'command': command,
            'output_file': output_file
        }
        return self.get(self.urls.get('abort').format(box), body=body)
