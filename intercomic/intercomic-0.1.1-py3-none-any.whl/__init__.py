from .client import Client
from requests.auth import AuthBase


__all__ = ['IntercomApp']

__version__ = '0.1.1'


class IntercomAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return r


class IntercomApp(Client):
    def __init__(self, access_token, *args, **kwargs):
        auth = IntercomAuth(access_token)
        super(IntercomApp, self).__init__(auth=auth, *args, **kwargs)
