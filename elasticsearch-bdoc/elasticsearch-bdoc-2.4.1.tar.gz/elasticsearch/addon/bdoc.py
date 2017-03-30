# -*- coding: utf-8 -*-

import time
import httplib
import sys

import hmac
import hashlib
import base64

accessKeyId = "d834d6f1ba581d74fb27"
secretAccessKey = "12b20a6fd9747ec6188d446df1fa5b04961dae35"


def timestamp():
    return long(time.time() * 1000)


def stringToSign(method, uri, date, contentType = None):
    if method is None or uri is None or date is None:
        raise RuntimeError("argement 'method', 'uri' and 'date' cannot be None.")
    if "?" in uri:
        uri = uri[:uri.index("?")]
    if contentType is not None:
        contentType = str.lower(contentType)
    if "multipart/form-data" in contentType:
        contentType = "multipart/form-data"
    else:
        contentType = ""
    return str.lower(str(method)) + "\n\n" + contentType + "\n" + str(date) + "\n" + uri


def sign(key, data):
    if key is None or data is None:
        raise RuntimeError("argument 'key' and 'data' cannot be None.")
    return base64.b64encode(hmac.new(key, msg=data, digestmod=hashlib.sha1).digest())



def getHeaders(method, uri):
    contentType = "application/json; charset=UTF-8"
    date = timestamp()
    signature = sign(secretAccessKey, stringToSign(method, uri, date, contentType))

    headers = {
        "Content-Type": contentType if contentType is not None else "",
        "BDOC-Date": date,
        "Authorization": "BDOC " + accessKeyId + ":" + signature
    }

    print headers
    return headers

