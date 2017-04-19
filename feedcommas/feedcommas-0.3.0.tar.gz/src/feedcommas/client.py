# Copyright (C) 2017 Michał Góral.
#
# This file is part of Feed Commas
#
# Feed Commas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Feed Commas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Feed Commas. If not, see <http://www.gnu.org/licenses/>.

'''Commafeed REST API client. Functions defined here Fetche and parse Commafeed
data.  This module is used as a communication endpoint by `content.Provider`.'''

import os
import collections
from urllib.parse import urlparse

import requests

import feedcommas.config as config
import feedcommas.model as model
from feedcommas.locale import _

_api_addr = None
_session = None


class ArticleMeta:
    '''Structure for holding articles and their metadata.'''
    def __init__(self):
        self.has_more = False
        self.articles = []


def init(user, password):
    '''Initializes module-wide variables in a worker process. Accepts
    password_cmd_out which should be evaluated by a master process (to avoid
    accidential execution of given command several times).'''
    global _api_addr
    global _session

    _api_addr = '%s/rest/' % config.get_value('server.address')

    _session = requests.Session()
    _session.auth = requests.auth.HTTPBasicAuth(user, password)

    # Well, obviously because we prepare a request by ourselves and we use a
    # session, proxy auto-detection of requests doesn't work.
    proxies = _get_proxies('http', 'https')
    if proxies:
        _session.proxies = proxies


class APIFailure(Exception):
    '''Base exception for errors indicated by Commafeed.'''
    pass


def login(username, password):
    '''Tries to login to CommaFeed. Returns whether login wass successfull'''
    resp = _post(_addr('/user/login'), name=username, password=password)
    return resp.status_code == 200


def get_articles(type_, **kwargs):
    '''Returns a list of entries gathered in Commafeed. This function
    abstracts Commafeed's implementation which splits getting category and
    feed entries to 2 different requests.'''
    resp = _get(_addr('/%s/entries' % type_), **kwargs)
    return _parse_entries(_json(resp))


def get_feeds():
    '''Returns a list of subscribed feeds.'''
    resp = _get(_addr('/category/get'))
    return _parse_feeds(_json(resp))


def mark(type_, **kwargs):
    '''Mark category or entry, depending on `type_`'''
    _post(_addr('/%s/mark' % type_), **kwargs)


def star(**kwargs):
    '''Star or unstar an entry.'''
    _post(_addr('/entry/star'), **kwargs)


def _get(addr, **kwargs):
    resp = _http_send('GET', addr, params=kwargs)
    if resp.status_code != 200:
        raise APIFailure(resp.text)
    return resp


def _post(addr, **kwargs):
    resp = _http_send('POST', addr, json=kwargs)
    if resp.status_code != 200:
        raise APIFailure(resp.text)
    return resp


def _addr(req_addr):
    return '%s/%s' % (_api_addr, req_addr)


def _http_send(*args, **kwargs):
    '''It's a wrapper for sending GET/POST requests, which handles redirects
    by itself. It's because `requests` don't resend Basic HTTP Auth data
    when redirect incomes. See their issue tracker for details:
    https://github.com/kennethreitz/requests/issues/2949.

    So we're just handle redirect by ourselves in more-less safe manner:
    redirect must be to the same domain and protocol must be the same.

    Usually, commafeed server redirects from e.g. commafeed.com to
    www.commafeed.com.

    All arguments and keyword arguments are passed directly to requests'
    Request object.'''
    def _cmp_netloc(old_netloc, new_netloc):
        return (new_netloc.endswith('.%s' % old_netloc) or
                old_netloc.endswith('.%s' % new_netloc))

    def _cmp_urls(old_url, new_url):
        old = urlparse(old_url)
        new = urlparse(new_url)
        return (old.scheme == new.scheme and
                _cmp_netloc(old.netloc, new.netloc))

    tmo = config.get_value('server.timeout')
    req = requests.Request(*args, **kwargs)
    prp = _session.prepare_request(req)
    resp = _session.send(prp, allow_redirects=False, timeout=tmo)

    while resp.is_redirect and _cmp_urls(prp.url, resp.headers['Location']):
        req.url = resp.headers['Location']
        prp = _session.prepare_request(req)
        resp = _session.send(prp, allow_redirects=False, timeout=tmo)

    return resp


def _get_proxies(*args):
    proxies = {}
    for name in args:
        env_name = '%s_proxy' % name
        proxy = os.getenv(env_name, os.getenv(env_name.upper()))
        if proxy:
            proxies[name] = proxy
    return proxies


def _json(resp):
    return resp.json(object_pairs_hook=collections.OrderedDict)


def _parse_feeds(data):
    def _extract_node(node, *args, **kwargs):
        return model.Feed(node['id'], node['name'], unread=node.get('unread'),
                          *args, **kwargs)

    # Commafeed returns a tree, so we'll simply use BFS to traverse it.
    root = _extract_node(data, is_category=True)
    queue = collections.deque([(root, data)])

    # Commafeed doesn't return a special 'starred' category, so we must hardcode
    # it.
    model.Feed('starred', _('Starred'), is_category=True, parent=root)

    while len(queue) > 0:
        parent, data_parent = queue.popleft()

        for ch in data_parent['children']:
            node = _extract_node(ch, is_category=True, parent=parent)
            queue.append((node, ch))

        for feed in data_parent['feeds']:
            _extract_node(feed, parent=parent)

    return root


def _parse_entries(data):
    meta = ArticleMeta()

    meta.has_more = data['entries']

    for entry in data['entries']:
        art = model.Article.from_json(entry)
        meta.articles.append(art)
    return meta
