import requests
from .common import APIBase


class AuthenticationError(Exception):
    """
    Represents an authentication error that occurred during ticket creation.
    """
    pass



class Authentication(APIBase):
    def __init__(self, base_url):
        APIBase.__init__(self, base_url, 'authentication', 'tickets')

    def create_ticket(self, user_id, password):
        credentials = {"userId": user_id, "password": password}

        try:
            return requests.post(self.path(), json=credentials)
        except requests.exceptions.ConnectionError:
            raise AuthenticationError('Unable to connect to ACS server')


