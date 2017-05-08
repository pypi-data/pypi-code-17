import json
import logging
from postman_client.exceptions import APIError
from apysignature.query_encoder import QueryEncoder
from apysignature.signature import Request as Request_sig, Token
from requests import Request, Session, ReadTimeout, ConnectTimeout, HTTPError

__author__ = 'thiagocdecastro'
__version__ = '0.1.12'
logging.basicConfig(format='%(asctime)s %(message)s')


def endpoint(method, endpoint):
    def decorator(func):
        def wrapped(self, *args, **kwargs):
            self.http_method = method
            self.endpoint = endpoint
            return func(self, *args, **kwargs)
        return wrapped
    return decorator


class Api(object):

    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'

    server_uri = ''
    urls = {}
    headers = {}
    endpoint = ''
    http_method = ''

    _api_key = ''
    _api_secret = ''

    def __init__(self, fail_silently=False):
        self._session = Session()
        self.fail_silently = fail_silently

    def set_header(self, header):
        """
        :type header: dict
        :return:
        """
        self.headers.update(header)

    def get_headers(self):
        return self.headers

    def query_encode(self, url, payload):
        if '?' not in url:
            url += '?'
        else:
            url += '&'
        for key, value in payload.iteritems():
            url += QueryEncoder.encode_param(key, str(value)) + '&'
        return url.rstrip('&')

    def sign_request(self, payload=None):
        if not payload:
            payload = {}
        request = Request_sig(self.http_method, self.endpoint, payload)
        token = Token(self._api_key, self._api_secret)
        auth = request.sign(token)
        return auth

    def request(self, method=None, url=None, headers=None, payload=None, timeout_connect=10, timeout_read=15):
        if not url:
            url = self.endpoint
        if not method:
            method = self.http_method
        if not headers:
            headers = self.headers
        timeout = (timeout_connect, timeout_read)

        url = self.server_uri + url

        # Generate and sign request URL
        auth = self.sign_request()
        if auth:
            url = self.query_encode(url, auth)

        if payload and method == 'GET':
            url = self.query_encode(url, payload)
            payload = None

        request = Request(
            method, url,
            json=payload,
            headers=headers
        )
        prepped = request.prepare()

        try:
            logging.info('EXTERNAL API: sending request on {0}'.format(url))
            response = self._session.send(prepped, timeout=timeout)
            valid_codes = (200, 201)

            if hasattr(response, 'status'):
                status_code = response.status
            else:
                status_code = response.status_code

            if response and status_code in valid_codes and response.content:
                response = json.loads(response.content)
            elif status_code not in valid_codes:
                logging.info("EXTERNAL API: request error: {0}".format(response.reason))
                if not self.fail_silently:
                    content = json.loads(response.content)
                    msg = content['error'] if 'error' in content else content['detail']
                    raise APIError(message_values=(msg.encode('utf8'),))
                response = None
            return response
        except (ReadTimeout, ConnectTimeout, HTTPError) as e:
            logging.info("EXTERNAL API: request error: {0}".format(e))
            if not self.fail_silently:
                raise e
            else:
                return None

    def sync_request(self, method, url, payload=None, headers=None):
        return self.request(method, url, payload, headers)
