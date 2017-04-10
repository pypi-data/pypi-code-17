from __future__ import unicode_literals

from wellaware.constants import Config, make_headers
from wellaware.base.base_resource import RestClient
from wellaware.exceptions import InvalidInputException
from token import Token


class Tokens(object):

    ENDPOINT = '/tokens'
    REST_CLIENT = RestClient()

    @classmethod
    def get_base_uri(cls, endpoint, **id_dict):
        if id_dict:
            return endpoint.format(**id_dict)
        return endpoint

    def login(self, username, password, expires=True, parameters={}):
        form_data = {'username': username, 'password': password, 'expires': expires}
        response = self.REST_CLIENT.post(
            self.get_base_uri(self.ENDPOINT), data=form_data, headers=Config.auth_headers, params=parameters
        )

        response = self.REST_CLIENT.handle_response(response)
        return Token(jwt=response.json()['token'])

    def impersonate(self, token, tenant_id=None, subject_id=None, role=None, expires=True, parameters={}):
        data = {'expires': expires}
        if tenant_id is not None and role is not None:
            data['tenantId'] = tenant_id
            data['role'] = role
        elif subject_id is not None:
            data['subjectId'] = subject_id
        else:
            raise InvalidInputException(422, "Must provide either tenant_id and role OR subject_id")

        response = self.REST_CLIENT.post(
            self.get_base_uri(self.ENDPOINT), data=data, headers=make_headers(token), params=parameters
        )

        response = self.REST_CLIENT.handle_response(response)
        return Token(jwt=response.json()['token'])
