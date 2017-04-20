# -*- coding: utf-8 -*-
from postman_client import endpoint, Api
from postman_client.exceptions import ImproperlyConfigured


class PostMan(Api):

    def __init__(self, key=None, secret=None, fail_silently=False, server_uri=None):
        super(PostMan, self).__init__(fail_silently)

        if server_uri:
            self.server_uri = server_uri
        else:
            self.server_uri = 'http://postman.alterdata.com.br'

        if not key:
            raise ImproperlyConfigured('A chave pública da API tem que ser passada no construtor')
        if not secret:
            raise ImproperlyConfigured('A chave privada da API tem que ser passada no construtor')

        self._api_key = key
        self._api_secret = secret

    @endpoint(Api.POST, '/api/send_mail/')
    def send(self, mail):
        response = self.request(payload=mail.get_payload())
        return response

    @endpoint(Api.POST, '/api/send_mail/template/')
    def send_template(self, mail):
        response = self.request(payload=mail.get_payload())
        return response
