#! /usr/bin/env python
# coding: utf-8

import hashlib
from datetime import datetime
import base64
import hmac
from JYAliYun import GMT_FORMAT

__author__ = 'ZhouHeng'

X_MNS_VERSION = "2016-06-06"


def mns_signature(access_key_secret, request_method, content_md5, content_type, request_time, x_headers, resource):
    if content_md5 is None:
        content_md5 = ""
    if content_type is None:
        content_type = ""
    x_headers_s = ""
    if x_headers is not None:
        if type(x_headers) == unicode:
            x_headers_s = x_headers
        elif type(x_headers) == dict:
            for key in sorted(x_headers.keys()):
                x_headers_s += key.lower() + ":" + x_headers[key] + "\n"
    msg = "%s\n%s\n%s\n%s\n%s%s" % (request_method, content_md5, content_type, request_time, x_headers_s, resource)
    h = hmac.new(access_key_secret, msg, hashlib.sha1)
    signature = base64.b64encode(h.digest())
    return signature


def construct_headers(access_id, access_key, request_method, content_type, x_headers, resource):
    request_time = datetime.utcnow().strftime(GMT_FORMAT)
    sign = mns_signature(access_key, request_method, "", content_type, request_time, x_headers, resource)
    headers = {"Authorization": "MNS %s:%s" % (access_id, sign), "Date": request_time}
    if isinstance(x_headers, dict):
        headers.update(x_headers)
    headers["Content-Type"] = content_type
    return headers
