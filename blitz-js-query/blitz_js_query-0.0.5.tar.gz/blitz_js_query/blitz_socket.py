from socketIO_client import SocketIO
from promise import Promise
import re


def on_socket(self, resolve):
    # Reset listeners for further connections
    self.socket.off('error')
    self.socket.off('connect')

    resolve(None)


def emit_lambda(self, resolve, reject, verb, query, data):
    # Remove port and http/s
    query = re.sub('http[s]?://', '', query)
    query = re.sub(':[0-9]+', '', query)

    # Post/put request
    if data:
        query = {
            'url': query,
            'body': data
        }

    # Emit
    self.socket.emit(verb, query, lambda x: resolve(x))
    self.socket.wait_for_callbacks(seconds=5)


class Socket:
    def __init__(self):
        self.socket = None

    """
    Attempts to connect to api with provided options
    """
    def config(self, auth_options, resolve, reject):
        # Close existing connections
        if self.socket:
            self.socket.disconnect()

        # Credentials provided?
        if auth_options.get('token'):
            self.socket = SocketIO(auth_options.get('api_url'), auth_options.get('api_port'),
                                   auth_options.get('namespace'),
                                   params={'query': 'bearer=' + auth_options.get('token'),
                                           'reconnect': True,
                                           'forceNew': True})
        # No credentials provided
        else:
            self.socket = SocketIO(auth_options.get('api_url'), auth_options.get('api_port'),
                                   auth_options.get('namespace'),
                                   params={'reconnect': True,
                                           'forceNew': True})

        # Resolve promise
        self.socket.on('connect', on_socket(self, resolve))

        # Invalid token?
        self.socket.on('error', on_socket(self, reject))

    """
    Send query, requests target endpoint, resolves promise with response
    """
    def send(self, verb, query, data):
        return Promise(lambda resolve, reject: emit_lambda(self, resolve, reject, verb, query, data))
