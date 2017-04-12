import requests
from .common import APIBase


class Authentication(APIBase):
    def __init__(self, base_url):
        APIBase.__init__(self, base_url, 'authentication', 'tickets')

    def create_ticket(self, user_id, password):
        credentials = {"userId": user_id, "password": password}

        try:
            response = requests.post(self.path(), json=credentials)
        except requests.exceptions.ConnectionError:
            print('Unable to connect to ACS server')
            return None

        return response

