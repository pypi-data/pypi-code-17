#! /usr/bin/env python
# coding: utf-8

import requests

__author__ = 'meisanggou'


def request(method, url, **kwargs):
    return requests.request(method, url, **kwargs)


def get(url, params=None, **kwargs):
    return request("GET", url, params=params, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request("POST", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    return request("PUT", url, data=data, **kwargs)


def delete(url, **kwargs):
    return request("DELETE", url, **kwargs)
