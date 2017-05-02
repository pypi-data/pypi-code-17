from .helpers import dict_merge
from pymitter import EventEmitter
from .connection import Connection
from promise import Promise
from socketIO_client import LoggingNamespace


def setup_connection_lambda(self):
    if self.options.get('use_socket'):
        self.client = self.connection.client.socket


def call_restful(self, method, query, data=None):
    # Put together the full URL
    query = self.options['api_url'] + ":" + self.options['api_port'] + query

    return Promise(lambda resolve, reject: self.connection.request(method, query, data)
                   .then(lambda res: resolve(res))
                   .catch(lambda err: reject(err)))


class Blitz(EventEmitter):
    def __init__(self, options):
        super().__init__()

        # Merge default options with client options
        self.options = {
            # Resource config
            "api_url": "http://localhost",
            "api_port": "3010",
            "auth_url": "http://localhost:3030/",

            # Connection Config
            "use_socket": True,
            "namespace": LoggingNamespace,

            # Authorization Config
            "user_key": None,
            "user_secret": None,
            "ignore_limiter": False
        }
        dict_merge(self.options, options)

        # Establish connection
        self.client = None
        self.connection = Connection()
        (self.connection.setup(self.options)
            # Open up client to higher level
            .then(lambda res: setup_connection_lambda(self))
            .then(lambda res: self.emit('ready')))

    """
    RESTful methods for manual interaction
    """
    def get(self, query):
        return call_restful(self, "GET", query)

    def post(self, query, data):
        return call_restful(self, "POST", query, data)

    def put(self, query, data):
        return call_restful(self, "PUT", query, data)

    def delete(self, query):
        return call_restful(self, "DELETE", query)
