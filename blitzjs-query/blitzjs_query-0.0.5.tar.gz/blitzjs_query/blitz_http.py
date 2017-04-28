import requests
from promise import Promise


class Http:
    def __init__(self):
        self.headers = {'user-agent': 'node-nexus-api/0.0.1'}

    """
    Sets new settings for http requests
    """
    def config(self, auth_options, resolve, reject):
        # Credentials provided?
        if auth_options.get('token'):
            self.headers['authorization'] = 'bearer ' + auth_options.get('token')

        resolve()

    """
    Send method, requests target endpoint, resolves promise with response
    """
    def send(self, method, query, data):
        return Promise(lambda resolve, reject: resolve(requests.request(method, query, data=data)))
