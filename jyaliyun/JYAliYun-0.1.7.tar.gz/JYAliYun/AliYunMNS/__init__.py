#! /usr/bin/env python
# coding: utf-8

from datetime import datetime
from JYAliYun import GMT_FORMAT
from JYAliYun.Tools import ali_signature

__author__ = 'ZhouHeng'

X_MNS_VERSION = "2016-06-06"


def construct_headers(access_id, access_key, request_method, content_type, x_headers, resource):
    request_time = datetime.utcnow().strftime(GMT_FORMAT)
    sign = ali_signature(access_key, request_method, "", content_type, request_time, x_headers, resource)
    headers = {"Authorization": "MNS %s:%s" % (access_id, sign), "Date": request_time}
    if isinstance(x_headers, dict):
        headers.update(x_headers)
    headers["Content-Type"] = content_type
    return headers
