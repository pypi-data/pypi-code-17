import base64
import hashlib
import hmac
import re
import time

import requests


def send_message():
    pass


class MNSResponse(object):
    __attrs__ = ['message_id', 'receipt_handler']

    def __init__(self, message_id, receipt_handler=None):
        self.message_id = message_id
        self.receipt_handler = receipt_handler

    def __str__(self):
        return self.message_id


class MNSClient(object):
    __attrs__ = ['ak', 'sk', 'endpoint', 'queue_name', 'path']

    def __init__(self, ak, sk, endpoint, queue_name):
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint,
        self.queue_name = queue_name
        self.path = '/queues/%s/messages' % self.queue_name

    def send(self, message):
        b64 = base64.b64encode(message.encode('utf-8')).decode()
        content = '<?xml version="1.0" encoding="UTF-8"?>' \
                  '<Message xmlns="http://mns.aliyuncs.com/doc/v1/"><MessageBody>%s</MessageBody></Message>' % b64

        response = self._call_api('POST', self.path, data=content)
        if 300 > response.status_code >= 200:
            msg_id = re.search('<MessageId>(.+?)</MessageId>', response.text)
            return msg_id

        return None

    def pop(self, wait_seconds=None, delete=False):
        path = self.path if wait_seconds is None else self.path + '?waitseconds=' + str(wait_seconds)
        response = self._call_api('GET', path)
        if 300 > response.status_code >= 200:
            handler = re.search('<ReceiptHandle>(.+?)</ReceiptHandle>', response.text).group(1)
            message_body = re.search('<MessageBody>(.+?)</MessageBody>', response.text).group(1)

            b64 = base64.b64decode(message_body).decode()
            if delete:
                self.delete(handler)
            return MNSResponse(b64, handler)

        return None

    def delete(self, handler):
        path = self.path + '?ReceiptHandle=' + handler
        self._call_api('DELETE', path)

    def _call_api(self, method, path, data=None):
        return requests.request(method, self.endpoint + path, data=data, headers=self._make_header(method, path))

    def _make_header(self, method, path):
        date_str = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        auth = base64.b64encode(
            hmac.new(self.sk,
                     (method + '\n\ntext/xml;charset=UTF-8\n' + date_str
                      + '\nx-mns-version:2015-06-06\n' + path).encode(),
                     hashlib.sha1).digest()).decode()

        headers = {'x-mns-version': '2015-06-06', 'date': date_str,
                   'Content-Type': 'text/xml;charset=UTF-8',
                   'Authorization': 'MNS %s:%s' % (self.ak, auth)}
        return headers
