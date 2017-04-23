#!/usr/bin/env python

from urllib.parse import urlencode
from urllib.request import Request, urlopen

def get(http_uri):
    return urlopen(http_uri).read()

def get_str(http_uri):
    return get(http_uri).decode('utf-8')

def post_form(http_uri, form_fields):
    post_request = Request(http_uri, urlencode(form_fields).encode())
    return urlopen(post_request).read().decode('utf-8')
