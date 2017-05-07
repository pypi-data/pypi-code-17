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

        resolve(None)

    """
    Send method, requests target endpoint, resolves promise with response
    """
    def send(self, method, query, data):
        if data:
            res = requests.request(method, query, json=data, headers=self.headers)
        else:
            res = requests.request(method, query, headers=self.headers)

        # Prepare object and send back
        response = {
            'statusCode': res.status_code,
            'sent': True,
            'body': res.text
        }
        return Promise(lambda resolve, reject: resolve(response))
