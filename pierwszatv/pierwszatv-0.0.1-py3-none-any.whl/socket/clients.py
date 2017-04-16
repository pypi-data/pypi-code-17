from socketIO_client import SocketIO, LoggingSocketIONamespace

from pierwszatv.socket.exceptions import PierwszaTvSocketError
from pierwszatv.socket.models import Stream


class PierwszaTvNamespace(LoggingSocketIONamespace):
    pass


class PierwszaTvSocket(SocketIO):

    def subscribe(self, stream_id):
        self.stream = None
        self.on('stream', self.on_stream)
        self.emit('subscribe', stream_id)
        self.wait(1)
        return self.stream

    def authorize(self, token):
        self.stoken = None
        self.on('authStatus', self.on_auth_status)
        self.emit('authorize', token)
        self.wait(1)
        return self.stoken

    def on_auth_status(self, data):
        if 'status' not in data or not data['status']:
            raise PierwszaTvSocketError

        self.stoken = data['stoken']

    def on_stream(self, data):
        if 'error' in data and data['error']:
            raise PierwszaTvSocketError

        self.stream = data


class PierwszaTvLiveSocket(SocketIO):

    def authorize(self, token):
        self.resp = None
        data = {'token': token}
        self.on('authStatus', self.on_auth_status)
        self.emit('authorize', data)
        self.wait(1)
        return self.resp

    def on_auth_status(self, data):
        self.resp = data
