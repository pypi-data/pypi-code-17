# from anchcloud.conn.auth import *
import base64
import httplib
import json
from datetime import datetime, timedelta
from urllib import urlencode
from urlparse import urlparse

import oauth2 as oauth

from anchcloud.iaas.errors import *


class APIConnection(object):
    def __init__(self, access_key_id, secret_access_key, endpoint="https://openapi.51idc.com", port=443, retry_count=3):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.port = port
        o = urlparse(endpoint)
        self.protocol = o.scheme
        self.host = o.netloc
        self.retry_count = retry_count
        self.gettoken_time = None
        self.expired_time = None
        self.token = None

    def check_token_exist(self):
        if self.token:
            return True
        return False

    def check_token_expired(self):
        if self.gettoken_time and self.expired_time:
            if datetime.now() < self.expired_time:
                return True
        return False

    def get_token(self):
        if self.check_token_exist() and self.check_token_expired():
            # print 22222
            return self.token
        consumer = oauth.Consumer(key=self.access_key_id, secret=self.secret_access_key)
        request_token_url = "https://" + self.host + "/v2/oauth2/token"
        grant_type = {"grant_type": "client_credentials"}
        client = oauth.Client(consumer)
        count = 0
        while (count < self.retry_count):
            resp, content = client.request(request_token_url, "POST", urlencode(grant_type), headers={
                'Authorization': 'Basic' + ' ' + base64.b64encode(self.access_key_id + ':' + self.secret_access_key)})
            if resp["status"] == "200":
                d = json.loads(content)
                self.token = d["access_token"]
                self.gettoken_time = datetime.now()
                self.expired_time = datetime.now() + timedelta(seconds=d['expires_in'] - 600)
                return self.token
            count += 1

    def send_request(self, verb, path, params, return_result=True):
        if not params:
            params = {}
        headers = {'Authorization': 'Bearer' + ' ' + self.get_token()}
        if verb == "POST" or verb == "PUT":
            params = json.dumps(params)
        else:
            params = urlencode(dict(params))
            path = "%s?%s" % (path, params)
        if self.protocol == "http":
            conn = httplib.HTTPConnection(self.host, self.port, timeout=30)
        else:
            conn = httplib.HTTPSConnection(self.host, self.port, timeout=30)
        conn.request(verb, path, params, headers)
        response = conn.getresponse()
        status = response.status
        result = response.read()
        if not result == "":
            result = json.loads(result)
        if status >= 200 and status < 300:
            if return_result:
                return result
            else:
                return True
        else:
            raise APIError(result["code"], result["message"])
