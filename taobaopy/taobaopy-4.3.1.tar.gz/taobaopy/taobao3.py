#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TaoBao Python SDK
~~~~~~~~~~~~~~~~~~~~~

usage:

   >>> from taobaopy.taobao import TaoBaoAPIClient
   >>> cli_ = TaoBaoAPIClient(__YOUR_APP_KEY__, __YOUR_APP_SECRET__)
   >>> r = cli_.item_get(num_iid='1234567', fields='num_iid,title,price,pic_url')
   >>> print r
"""
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

__author__ = 'Fred Wang (taobao-pysdk@1e20.com)'
__title__ = 'taobaopy'
__version__ = '4.5.0'
__license__ = 'BSD License'
__copyright__ = 'Copyright 2013-2014 Fred Wang'

import sys
import json
import time
import hmac
import math
import requests
import logging
from datetime import datetime
from future.utils import iteritems
from builtins import bytes, str as text

if (sys.version_info > (3, 0)):
    is_py3 = True
else:
    is_py3 = False

api_logger = logging.getLogger(__name__)
api_logger.addHandler(logging.NullHandler())

RETRY_SUB_CODES = {
    'isp.top-remote-connection-timeout',
    'isp.top-remote-connection-timeout-tmall',
    'isp.top-remote-service-unavailable',
    'isp.top-remote-service-unavailable-tmall',
    'isp.top-remote-connection-control-error',
    'isp.top-remote-connection-control-error-tmall',
    'isp.top-remote-unknown-error',
    'isp.top-remote-unknown-error-tmall',
    'isp.remote-connection-error',
    'isp.remote-connection-error-tmall',
    'isp.item-update-service-error:GENERIC_FAILURE',
    'isp.item-update-service-error:IC_SYSTEM_NOT_READY_TRY_AGAIN_LATER',
    'ism.json-decode-error',
    'ism.demo-error',
}

if is_py3:  # py 3+
    VALUE_TO_STR = {
        type(datetime.now()): lambda v: v.strftime('%Y-%m-%d %H:%M:%S'),
        type(u'a'): lambda v: v,
        type(0.1): lambda v: "%.2f" % v,
        type(True): lambda v: str(v).lower(),
    }

    DEFAULT_VALUE_TO_STR = lambda x: str(x)
else: # py 2+
    VALUE_TO_STR = {
        type(datetime.now()): lambda v: v.strftime('%Y-%m-%d %H:%M:%S'),
        type(u'a'): lambda v: v.encode("utf-8"),
        type(0.1): lambda v: "%.2f" % v,
        type(True): lambda v: str(v).lower(),
    }
    DEFAULT_VALUE_TO_STR = lambda x: str(x)


class BaseAPIRequest(object):
    """The Base API Request"""

    def __init__(self, url, client, values):
        self.url = url
        self.values = values
        self.client = client
        self.key = client.client_id
        self.sec = client.client_secret
        self.retry_sub_codes = client.retry_sub_codes

    def sign(self):
        """Return encoded data and files
        """
        data, files = {}, {}
        if not self.values:
            raise NotImplementedError('no values')
        args = {'app_key': self.key, 'sign_method': 'hmac', 'format': 'json', 'v': '2.0', 'timestamp': datetime.now()}

        for k, v in list(dict(self.values, **args).items()):
            kk = k.replace('__', '.')
            if hasattr(v, 'read'):
                files[kk] = v
            elif v is not None:
                data[kk] = VALUE_TO_STR.get(type(v), DEFAULT_VALUE_TO_STR)(v)

        args_str = "".join(["{}{}".format(k, data[k]) for k in sorted(data.keys())])
        sign = hmac.new(bytes(self.sec, "ascii"), bytes(args_str, "utf-8"))

        data['sign'] = sign.hexdigest().upper()
        return data, files

    def run(self):
        ts_start = time.time()
        data, files = self.sign()
        ret = {}
        retry_count = self.client.retry_count
        for try_id in range(retry_count):
            ret = self.open(data, files)
            for file in list(files.values()):
                file.seek(0)
            if 'error_response' in ret:
                sub_code = ret['error_response'].get('sub_code')
                if sub_code in self.retry_sub_codes:
                    continue
                elif sub_code == 'accesscontrol.limited-by-api-access-count':
                    if try_id < retry_count - 1:
                        ts_sleep = 0.1 * math.pow(2, try_id)
                        time.sleep(ts_sleep)
                        logging.warn("meet access-control, sleep %.3lf seconds", ts_sleep)
                    continue
            break
        ts_used = (time.time() - ts_start) * 1000
        method = data.get('method', '')
        files2 = dict([(k, str(v)) for k, v in iteritems(files)])
        data.update(**files2)
        log_data = '%.2fms [{>.<}] %s [{>.<}] %s [{>.<}] %s' % (
            ts_used, method, json.dumps(data), json.dumps(ret))

        if 'error_response' in ret:
            api_logger.warning(log_data)
            r = ret['error_response']
            raise TaoBaoAPIError(data, **r)
        elif method.startswith("taobao.ump") or method.startswith("taobao.promotion"):
            api_logger.info(log_data)
        else:
            api_logger.debug(log_data)

        return ret

    def open(self, data, files):
        raise NotImplemented


class DefaultAPIRequest(BaseAPIRequest):
    """The Basic API Request"""
    def __init__(self, url, client, values):
        super(DefaultAPIRequest, self).__init__(url, client, values)
        self._session = None

    @property
    def session(self):
        if not self._session:
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            self._session = s
        return self._session

    def open(self, data, files):
        for t in range(3, -1, -1):
            r = None
            try:
                r = self.session.post(self.url, data, files=files, headers={'Accept-Encoding': 'gzip'})
                break
            except ConnectionError as e:
                if t == 0:
                    raise

        try:
            return r.json()
        except ValueError:
            try:
                text = r.text.replace('\t', '\\t').replace('\n', '\\n').replace('\r', '\\r')
                return json.loads(text)
            except ValueError as e:
                return {
                    "error_response": {"msg": "json decode error", "sub_code": "ism.json-decode-error",
                                       "code": 15, "sub_msg": "json-error: %s || %s" % (str(e), r.text)}}


class TaoBaoAPIError(Exception):
    """raise APIError if got failed json message."""

    def __init__(self, request, code='', msg='', sub_code='', sub_msg='', request_id='', **kwargs):
        """TaoBao SDK Error, Raised From TaoBao"""
        self.request = request
        self.code = code
        self.msg = msg
        self.sub_code = sub_code
        self.sub_msg = sub_msg
        self.request_id = request_id
        Exception.__init__(self, self.__str__())

    def __repr__(self):
        return "{code}|{msg}|{sub_code}|{request_id}|{sub_msg}{request}".format(
            code=self.code, msg=self.msg, sub_code=self.sub_code, sub_msg=self.sub_msg,
            request_id=self.request_id, request=self.request)


    def __str__(self):
        """Build String For All the Request and Response"""
        return "{code}|{msg}|{sub_code}|{request_id}|{sub_msg}".format(
            code=self.code, msg=self.msg, sub_code=self.sub_code, sub_msg=self.sub_msg,
            request_id=self.request_id, request=self.request)

    def str2(self):
        """Build String For the Request only"""
        return "{code}|{msg}|{sub_code}|{request_id}|{sub_msg}".format(
            code=self.code, msg=self.msg, sub_code=self.sub_code, sub_msg=self.sub_msg,
            request_id=self.request_id, request=self.request)


class HttpObject(object):
    def __init__(self, client):
        self.client = client

    def __getattr__(self, attr):
        def wrap(**kw):
            if attr.find('__') >= 0:
                attr2 = attr.split('__', 2)
                method = attr2[0] + '.' + attr2[1].replace('_', '.')
            else:
                method = "taobao." + attr.replace('_', '.')
            kw['method'] = method
            if not self.client.is_expires():
                kw['session'] = self.client.access_token
            req = self.client.fetcher_class(self.client.gw_url, self.client, kw)
            return req.run()

        return wrap


class TaoBaoAPIClient(object):
    """API client using synchronized invocation."""

    def __init__(self, app_key, app_secret, domain='gw.api.taobao.com', fetcher_class=DefaultAPIRequest,
                 retry_sub_codes=None, retry_count=5, **kw):
        """Init API Client"""
        self.client_id = app_key
        self.client_secret = app_secret
        self.gw_url = 'http://%s/router/rest' % (domain,)
        self.access_token = None
        self.expires = 0.0
        self.fetcher_class = fetcher_class
        self.get = HttpObject(self)
        self.post = HttpObject(self)
        self.upload = HttpObject(self)
        self.retry_sub_codes = retry_sub_codes if retry_sub_codes else RETRY_SUB_CODES
        self.retry_count = retry_count

    def set_access_token(self, access_token, expires_in=2147483647):
        """Set Default Access Token To This Client"""
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def set_fetcher_class(self, fetcher_class):
        """Set Fetcher Class"""
        self.fetcher_class = fetcher_class

    def is_expires(self):
        """Check Token expires"""
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.post, attr)


APIClient = TaoBaoAPIClient
APIError = TaoBaoAPIError
