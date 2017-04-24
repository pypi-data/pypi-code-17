import requests


class RPCProxy(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def __call__(self, **kwargs):
        try:
            resp = self.client.session.post(self.client.endpoint,
                                            data=json.dumps(kwargs),
                                            headers={'X-Rpc-Action': self.name},
                                           )
        except:
            raise
        return resp.json()


class RPCClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def __getattr__(self, key):
        return RPCProxy(self, name)
