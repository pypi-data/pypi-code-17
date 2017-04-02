import requests
from .common import APIBase


class People(APIBase):
    def __init__(self, base_url):
        # alfresco = 'core' API
        APIBase.__init__(self, base_url, 'alfresco', 'people')

    def create_person(self, ticket, user_name, password, email, first_name):
        person = {
            'id': user_name,
            'firstName': first_name,
            'password': password,
            'email': email
        }
        headers = self.auth_header(ticket)
        response = requests.post(self.path(), json=person, headers=headers)
        return response
