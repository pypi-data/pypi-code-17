import json
import logging

from amqp import RpcClient

class VisaRpcClient(RpcClient):
    def __init__(self, username, password, name='query', exchange='visa_rpc', host='localhost', port=5432):
        RpcClient.__init__(self, host=host, name=name, exchange=exchange, username=username, password=password, port=port)
        self.name = name
        self.declare_method(self.on_response)

    def toMessage(self, alias, command):
        return {'alias': alias, 'command': command}

    def fromMessage(self, response):
        return response['result']

    def alias(self, request):
        logging.info('REMOTE.alias request ' + json.dumps(obj=request, ensure_ascii=False))
        return self.call(body=request, method_name='alias')

    def query(self, alias, command):
        request = self.toMessage(alias, command)
        logging.info('REMOTE.query request ' + json.dumps(obj=request, ensure_ascii=False))
        response = self.call(body=request, method_name='query')
        return self.fromMessage(response);

    def read(self, alias, command):
        request = self.toMessage(alias, command)
        logging.info('REMOTE.read request ' + json.dumps(obj=request, ensure_ascii=False))
        response = self.call(body=request, method_name='read')
        return self.fromMessage(response);

    def write(self, alias, command):
        request = self.toMessage(alias, command)

        logging.info('REMOTE.write request ' + json.dumps(obj=request, ensure_ascii=False))
        return self.call(body=request, method_name='write')

    def list(self):
        logging.info('REMOTE.list request ')
        return self.call(method_name='list', body=json.dumps(obj={}, ensure_ascii=False))