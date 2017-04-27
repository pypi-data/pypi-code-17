# -*- coding: utf-8 -*-
import requests

from fastrpc.utils import parse_collection_file, pp


def load(collection):
    return parse_collection_file(collection)


def gather_requests(collection):
    request_json = load(collection)
    pp.pprint(request_json)
    for request in request_json['requests']:
        if request['method'] in ('POST', 'PUT'):
            post(request)
        elif request['method'] == 'GET':
            get(request)


def get(request):
    url = request['url']
    resp = requests.get(url)
    return resp


def post(request):
    payload = eval(request['rawModeData'])
    url = request['url']
    resp = requests.post(url, data=payload)
    return resp
