import crypto
import json
import re
import requests
import time


class Rest(object):

    def __init__(self, base_url, account=None):
        self.base_url = base_url
        self.host = re.split('[:/]*', self.base_url)[1]
        self.account = account
        self.methods = {}
        self.methods['GET']     = requests.get
        self.methods['POST']    = requests.post
        self.methods['PUT']     = requests.put
        self.methods['DELETE']  = requests.delete
        self.methods['PATCH']   = requests.patch
        self.methods['OPTIONS'] = requests.options

    def get(self, url):
        if url.startswith("/all/") or url.startswith("/auth/"):
            return self.server_call(url)
        return self.auth_server_call("GET", url)

    def server_call(self, url, headers={'Accept': 'application/json'}):
        try:
            return requests.get(self.base_url + url, headers=headers)
        except Exception as err:
            print "Error on REST call {} \n {}".format(self.base_url + url, err)

    def sparse_json(self, body=None):
        if body is None:
            return None
        result = json.dumps(body, separators=(',', ':'))
        return None if result == '{}' else result

    def canonical(self, body=None):
       return None if body is None else json.loads(body)

    def auth_server_call(self, method, url, body=None):
        assert self.account is not None, "Call to server requiring auth needs account"
        try:
            canonical_body = self.canonical(body)
            sparse_body    = self.sparse_json(canonical_body)
            headers        = self.get_headers(method, url, sparse_body)
            method         = self.methods[method]

            return method(url=self.base_url + url, json=canonical_body, headers=headers)
        except Exception as err:
            print "Error on REST call {} \n {}".format(self.base_url + url, err)

    def get_headers(self, method, url, body):
        nonce = str(long(time.time() * 1000))
        headers = crypto.get_headers(self.account.user_id, self.account.shared_secret, nonce, method, url, body)
        headers['Host'] = self.host
        return headers
