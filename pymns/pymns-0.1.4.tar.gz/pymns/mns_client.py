import base64
import hashlib
import hmac
import re
import time

import requests


def send_message():
    pass


def _parse_simple_xml(xml):
    matches = re.findall(r'<(.+?)>(.+?)</\1>', xml)
    return {x[0]: x[1] for x in matches}


class Message(object):
    __attrs__ = ['message_id', 'receipt_handle', 'message_body_md5',
                 'message_body', 'enqueue_time', 'next_visible_time',
                 'first_dequeue_time', 'dequeue_count', 'priority']

    def __init__(self, message):
        xml = _parse_simple_xml(message)
        self.message_id = xml.get('MessageId')
        self.receipt_handle = xml.get('ReceiptHandle')
        self.message_body_md5 = xml.get('MessageBodyMD5')
        self.message_body_raw = xml.get('MessageBody')
        self.message_body = base64.b64decode(self.message_body_raw).decode() if self.message_body_raw else None
        self.enqueue_time = xml.get('EnqueueTime')
        self.next_visible_time = xml.get('NextVisibleTime')
        self.first_dequeue_time = xml.get('FirstDequeueTime')
        self.dequeue_count = xml.get('DequeueCount')
        self.priority = xml.get('Priority')

    def __str__(self):
        return self.message_id


class MNSClient(object):
    __attrs__ = ['ak', 'sk', 'endpoint', 'queue_name', 'path',
                 'delay_seconds', 'max_message_size', 'message_retention_period',
                 'visibility_timeout', 'polling_wait_seconds', 'logging_enable']

    def __init__(self, ak, sk, endpoint, queue_name):
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint
        self.queue_name = queue_name
        self.path = '/queues/%s/messages' % self.queue_name
        self.delay_seconds = 0
        self.max_message_size = 65536
        self.message_retention_period = 345600
        self.visibility_timeout = 30
        self.polling_wait_seconds = 0
        self.logging_enable = False

    def send(self, message):
        b64 = base64.b64encode(message.encode('utf-8')).decode()
        response = self._call_api('POST', self.path, ns='Message', attrs={'MessageBody': b64})
        if 300 > response.status_code >= 200:
            return Message(response.text)

        return None

    def get_info(self):
        path = '/queues/' + self.queue_name
        response = self._call_api('GET', path)
        if response.status_code == 200:
            xml = _parse_simple_xml(response.text)
            self.delay_seconds = xml.get('DelaySeconds')
            self.max_message_size = xml.get('MaximumMessageSize')
            self.message_retention_period = xml.get('MessageRetentionPeriod')
            self.polling_wait_seconds = xml.get('PollingWaitSeconds')
            return xml

        return dict()

    def set_attr(self):
        path = '/queues/%s?metaoverride=true' % self.queue_name
        response = self._call_api('PUT', path, attrs={
            'DelaySeconds': self.delay_seconds,
            'PollingWaitSeconds': self.polling_wait_seconds,
            'VisibilityTimeout': self.visibility_timeout,
            'MaximumMessageSize': self.max_message_size,
            'MessageRetentionPeriod': self.message_retention_period,
            'LoggingEnabled': self.logging_enable
        })
        return response.status_code == 204

    def create_queue(self):
        response = self._call_api('PUT', '/queues/' + self.queue_name, attrs={
            'DelaySeconds': self.delay_seconds,
            'PollingWaitSeconds': self.polling_wait_seconds,
            'VisibilityTimeout': self.visibility_timeout,
            'MaximumMessageSize': self.max_message_size,
            'MessageRetentionPeriod': self.message_retention_period,
            'LoggingEnabled': self.logging_enable,
        })

        if response.status_code in (201, 204):
            return 0
        elif response.status_code == 409:
            return 1

    def delete_queue(self):
        path = '/queues/%s' % self.queue_name
        response = self._call_api('DELETE', path)
        return response.status_code == 204

    def batch_pop_messages(self, num, wait_seconds=None):
        path = '/queues/%s/messages?numOfMessages=%s&waitseconds=%s' % (self.queue_name, num, wait_seconds) \
            if wait_seconds is not None else '/queues/%s/messages?numOfMessages=%s' % (self.queue_name, num)

        response = self._call_api('GET', path)
        if 300 > response.status_code >= 200:
            messages = re.findall(r'<Message>(.+?)</Message>', response.text.replace('\n', ''))
            return [Message(x) for x in messages]

        return []

    def batch_delete(self, handlers):
        response = self._call_api('DELETE', self.path, ns='ReceiptHandles',
                                  attrs=[{'ReceiptHandle': x} for x in handlers])
        if response.status_code == 204:
            return handlers

        # todo parse errors
        return []

    def peek(self):
        path = self.path + '?peekonly=true'
        response = self._call_api('GET', path)
        return Message(response.text)

    def pop(self, wait_seconds=None, delete=False):
        path = self.path if wait_seconds is None else self.path + '?waitseconds=' + str(wait_seconds)
        response = self._call_api('GET', path)
        if 300 > response.status_code >= 200:
            message = Message(response.text)
            if delete:
                self.delete(message.receipt_handle)
            return message

        return None

    def reset(self, handler, seconds=0):
        path = '/queues/%s/messages?receiptHandle=%s&visibilityTimeout=%s' % (self.queue_name, handler, seconds)
        response = self._call_api('PUT', path)
        if response.status_code == 200:
            return Message(response.text)

        return None

    def delete(self, handler):
        path = self.path + '?ReceiptHandle=' + handler
        self._call_api('DELETE', path)

    def _call_api(self, method, path, data=None, ns='Queue', attrs=None):
        if data is None and attrs:
            data = self._make_request(ns, attrs)

        response = requests.request(method, self.endpoint + path, data=data, headers=self._make_header(method, path))
        if response.status_code == 403:
            raise ValueError('ak or sk invalid')

        return response

    def _make_header(self, method, path):
        date_str = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        auth = base64.b64encode(
            hmac.new(self.sk.encode(),
                     (method + '\n\ntext/xml;charset=UTF-8\n' + date_str
                      + '\nx-mns-version:2015-06-06\n' + path).encode(),
                     hashlib.sha1).digest()).decode()

        headers = {'x-mns-version': '2015-06-06', 'date': date_str,
                   'Content-Type': 'text/xml;charset=UTF-8',
                   'Authorization': 'MNS %s:%s' % (self.ak, auth)}
        return headers

    @staticmethod
    def _make_request(ns, attrs):
        if isinstance(attrs, dict):
            return '<?xml version="1.0" encoding="UTF-8"?>\n<%s xmlns="http://mns.aliyuncs.com/doc/v1/">\n%s</%s>' \
                   % (ns, '\n'.join(['<%s>%s</%s>' % (k, v, k) for k, v in attrs.items()]), ns)
        else:
            args = []
            for item in attrs:
                for k, v in item:
                    args.append('<%s>%s</%s>' % (k, v, k))

            return '<?xml version="1.0" encoding="UTF-8"?>\n<%s xmlns="http://mns.aliyuncs.com/doc/v1/">\n%s</%s>' \
                   % (ns, '\n'.join(args), ns)
