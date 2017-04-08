#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from textile import Textile

import six
from six.moves import urllib
urlsplit, urlunsplit, quote, unquote = (
        urllib.parse.urlsplit, urllib.parse.urlunsplit, urllib.parse.quote,
        urllib.parse.unquote
        )

try:
    import regex as re
except ImportError:
    import re


class RawLink(Textile):
    """Just like Textile, but use the raw link input instead of
    percent-encoding it."""
    def __init__(self, rawlink=True, **kwargs):
        super(RawLink, self).__init__(**kwargs)
        self.rawlink = rawlink

    def encode_url(self, url):
        """
        Converts a (unicode) URL to an ASCII URL, with the domain part
        IDNA-encoded and the path part %-encoded (as per RFC 3986).

        Fixed version of the following code fragment from Stack Overflow:
            http://stackoverflow.com/a/804380/72656
        """
        # turn string into unicode
        if not isinstance(url, six.text_type):
            url = url.decode('utf8')

        # parse it
        parsed = urlsplit(url)

        if parsed.netloc:
            # divide the netloc further
            netloc_pattern = re.compile(r"""
                (?:(?P<user>[^:@]+)(?::(?P<password>[^:@]+))?@)?
                (?P<host>[^:]+)
                (?::(?P<port>[0-9]+))?
            """, re.X | re.U)
            netloc_parsed = netloc_pattern.match(parsed.netloc).groupdict()
        else:
            netloc_parsed = {'user': '', 'password': '', 'host': '', 'port':
                             ''}

        # encode each component
        scheme = parsed.scheme
        user = netloc_parsed['user'] and quote(netloc_parsed['user'])
        password = (netloc_parsed['password'] and
                    quote(netloc_parsed['password']))
        host = netloc_parsed['host']
        port = netloc_parsed['port'] and netloc_parsed['port']
        path = '/'.join(
            urllib.parse.quote(urllib.parse.unquote(pce).encode('utf8'), b'')
            for pce in parsed.path.split('/')
        )
        # The above quote function percent-encodes the path.  If we're using
        # rawlink=True, unquote it to get the raw link back.
        if self.rawlink:
            path = unquote(path)

        query = quote(unquote(parsed.query), b'=&?/')
        fragment = quote(unquote(parsed.fragment))

        # put it back together
        netloc = ''
        if user:
            netloc = '{0}{1}'.format(netloc, user)
            if password:
                netloc = '{0}:{1}'.format(netloc, password)
            netloc = '{0}@'.format(netloc)
        netloc = '{0}{1}'.format(netloc, host)
        if port:
            netloc = '{0}:{1}'.format(netloc, port)
        return urlunsplit((scheme, netloc, path, query, fragment))


def textile(text):
    return RawLink().parse(text)
