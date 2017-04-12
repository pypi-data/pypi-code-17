from .auth import Authentication
from .people import People
from .sites import Sites
from .common import Nodes

class Client(object):
    def __init__(self, base_url):
        self.apis = {
            'auth': Authentication(base_url),
            'people': People(base_url),
            'sites': Sites(base_url),
            'nodes': Nodes(base_url)
        }

    def __getattr__(self, item):
        return self.apis.get(item)

