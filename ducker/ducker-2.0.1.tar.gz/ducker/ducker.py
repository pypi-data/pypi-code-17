#!/usr/bin/env python3
# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2016 Arun Prakash Jana <engineerarun@gmail.com>
# Copyright (C) 2016-2017 Jorge Maldonado Ventura <jorgesumle@freakspot.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import atexit
import collections
import functools
import gzip
import html.entities
import html.parser
import http.client
from http.client import HTTPSConnection
import socket
import ssl
import logging
import os
import signal
import sys
import textwrap
import urllib.parse
import webbrowser

from . import __version__

# Python optional dependency compatibility layer
try:
    import readline
except ImportError:
    pass

PROGRAM_DESCRIPTION = 'search with DuckDuckGo from the command line'

COLORMAP = {k: '\x1b[%sm' % v for k, v in {
    'a': '30', 'b': '31', 'c': '32', 'd': '33',
    'e': '34', 'f': '35', 'g': '36', 'h': '37',
    'i': '90', 'j': '91', 'k': '92', 'l': '93',
    'm': '94', 'n': '95', 'o': '96', 'p': '97',
    'A': '30;1', 'B': '31;1', 'C': '32;1', 'D': '33;1',
    'E': '34;1', 'F': '35;1', 'G': '36;1', 'H': '37;1',
    'I': '90;1', 'J': '91;1', 'K': '92;1', 'L': '93;1',
    'M': '94;1', 'N': '95;1', 'O': '96;1', 'P': '97;1',
    'x': '0', 'X': '1', 'y': '7', 'Y': '7;1',
}.items()}

# Disguise as Firefox on Ubuntu
USER_AGENT = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0')

# Logging for debugging purposes
logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger()


def sigint_handler(signum, frame):
    print('\nInterrupted.', file=sys.stderr)
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)


def printerr(msg):
    """Print message, verbatim, to stderr.
    ``msg`` could be any stringifiable value.
    """
    print(msg, file=sys.stderr)


class TLS1_2Connection(HTTPSConnection):
    """Overrides HTTPSConnection.connect to specify TLS version
    NOTE: TLS 1.2 is supported from Python 3.4
    """

    def __init__(self, host, **kwargs):
        HTTPSConnection.__init__(self, host, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port),
                self.timeout, self.source_address)

        # Optimizations not available on OS X
        if sys.platform.startswith('linux'):
            sock.setsockopt(socket.SOL_TCP, socket.TCP_DEFER_ACCEPT, 1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,524288)

        if getattr(self, '_tunnel_host', None):
            self.sock = sock
            self._tunnel()
            HTTPSConnection.connect(self)
        elif sys.version_info >= (3, 4):
            # Use TLS 1.2
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                    ssl_version=ssl.PROTOCOL_TLSv1_2)
        else:
            HTTPSConnection.connect(self)


class DdgUrl(object):
    """
    This class constructs the DuckDuckGo Search URL.
    This class is modelled on urllib.parse.ParseResult for familiarity,
    which means it supports reading of all six attributes -- scheme,
    netloc, path, params, query, fragment -- of
    urllib.parse.ParseResult, as well as the geturl() method.
    However, the attributes (properties) and methods listed below should
    be the preferred methods of access to this class.
    Parameters
    ----------
    opts : dict or argparse.Namespace, optional
        See the ``opts`` parameter of `update`.
    Other Parameters
    ----------------
    See "Other Parameters" of `update`.
    Attributes
    ----------
    hostname : str
        Read-write property.
    keywords : str or list of strs
        Read-write property.
    url : str
        Read-only property.
    Methods
    -------
    full()
    relative()
    update(opts=None, **kwargs)
    set_queries(**kwargs)
    unset_queries(*args)
    next_page()
    prev_page()
    first_page()
    """

    def __init__(self, opts=None, **kwargs):
        self.scheme = 'https'
        # self.netloc is a calculated property
        self.path = '/html/'
        self.params = ''
        # self.query is a calculated property
        self.fragment = ''

        self._reg = None
        self._num = 10
        self._start = 0
        self._keywords = []
        self._site = None
        self._query_dict = {
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'k1': '-1',
        }
        self.update(opts, **kwargs)

    def __str__(self):
        return self.url

    @property
    def url(self):
        """The full DuckDuckGo URL you want."""
        return self.full()

    @property
    def hostname(self):
        """The hostname."""
        return self.netloc

    @hostname.setter
    def hostname(self, hostname):
        self.netloc = hostname

    @property
    def keywords(self):
        """The keywords, either a str or a list of strs."""
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    def full(self):
        """Return the full URL.
        Returns
        -------
        str
        """
        url = (self.scheme + ':') if self.scheme else ''
        url += '//' + self.netloc + self.relative()
        return url

    def relative(self):
        """Return the relative URL (without scheme and authority).
        Authority (see RFC 3986 section 3.2), or netloc in the
        terminology of urllib.parse, basically means the hostname
        here. The relative URL is good for making HTTP(S) requests to a
        known host.
        Returns
        -------
        str
        """
        rel = self.path
        if self.params:
            rel += ';' + self.params
        if self.query:
            rel += '?' + self.query
        if self.fragment:
            rel += '#' + self.fragment
        return rel

    def update(self, opts=None, **kwargs):
        """Update the URL with the given options.
        Parameters
        ----------
        opts : dict or argparse.Namespace, optional
            Carries options that affect the DuckDuckGo Search URL. The
            list of currently recognized option keys with expected value
            types:
                duration: str (DdgArgumentParser.is_duration)
                exact: bool
                keywords: str or list of strs
                num: int
                site: str
                start: int
                reg: str
        Other Parameters
        ----------------
        kwargs
            The `kwargs` dict extends `opts`, that is, options can be
            specified either way, in `opts` or as individual keyword
            arguments.
        """

        if opts is None:
            opts = {}
        if hasattr(opts, '__dict__'):
            opts = opts.__dict__
        opts.update(kwargs)

        qd = self._query_dict
        if 'duration' in opts and opts['duration']:
            qd['df'] = opts['duration']
        if 'exact' in opts:
            if opts['exact']:
                qd['norw'] = 1
            else:
                qd.pop('norw', None)
        if 'keywords' in opts:
            self._keywords = opts['keywords']
        if 'num' in opts:
            self._num = opts['num']
        if 'site' in opts:
            self._site = opts['site']
        if 'start' in opts:
            self._start = opts['start']
        if 'reg' in opts:
            self._reg = opts['reg']
            qd['kl'] = opts['reg']

    def set_queries(self, **kwargs):
        """Forcefully set queries outside the normal `update` mechanism.
        Other Parameters
        ----------------
        kwargs
            Arbitrary key value pairs to be set in the query string. All
            keys and values should be stringifiable.
            Note that certain keys, e.g., ``q``, have their values
            constructed on the fly, so setting those has no actual
            effect.
        """
        for k, v in kwargs.items():
            self._query_dict[k] = v

    def unset_queries(self, *args):
        """Forcefully unset queries outside the normal `update` mechanism.
        Other Parameters
        ----------------
        args
            Arbitrary keys to be unset. No exception is raised if a key
            does not exist in the first place.
            Note that certain keys, e.g., ``q``, are always included in
            the resulting URL, so unsetting those has no actual effect.
        """
        for k in args:
            self._query_dict.pop(k, None)

    def next_page(self):
        """Navigate to the next page."""
        self._start += self._num

    def prev_page(self):
        """Navigate to the previous page.
        Raises
        ------
        ValueError
            If already at the first page (``start=0`` in the current
            query string).
        """
        if self._start == 0:
            raise ValueError('Already at the first page.')
        self._start = (self._start - self._num) if self._start > self._num else 0

    def first_page(self):
        """Navigate to the first page.
        Raises
        ------
        ValueError
            If already at the first page (``start=0`` in the current
            query string).
        """
        if self._start == 0:
            raise ValueError('Already at the first page.')
        self._start = 0

    @property
    def netloc(self):
        """The hostname."""
        return 'duckduckgo.com'

    @property
    def query(self):
        """The query string."""
        qd = {}
        qd.update(self._query_dict)
        qd['num'] = self._num
        qd['start'] = self._start

        # Construct the q query
        q = ''
        keywords = self._keywords
        if keywords:
            if isinstance(keywords, list):
                q += '+'.join([urllib.parse.quote_plus(kw) for kw in keywords])
            else:
                q += urllib.parse.quote_plus(keywords)
        if self._site:
            q += '+site:' + urllib.parse.quote_plus(self._site)
        if 'norw' in qd:
            qd['q'] = '"' + q + '"'
        else:
            qd['q'] = q

        return '&'.join(['%s=%s' % (k, qd[k]) for k in sorted(qd.keys())])


class DDGConnectionError(Exception):
    pass


class DdgConnection(object):
    """
    This class facilitates connecting to and fetching from DuckDuckGo.
    Parameters
    ----------
    See http.client.HTTPSConnection for documentation of the
    parameters.
    Raises
    ------
    DDGConnectionError
    Attributes
    ----------
    host : str
        The currently connected host. Read-only property. Use
        `new_connection` to change host.
    Methods
    -------
    new_connection(host=None, port=None, timeout=45)
    renew_connection(timeout=45)
    fetch_page(url)
    close()
    """

    def __init__(self, host, port=None, timeout=45, proxy=None):
        self._host = None
        self._port = None
        self._proxy = proxy
        self._conn = None
        self.new_connection(host, port=port, timeout=timeout)
        self.cookie = ''

    @property
    def host(self):
        """The host currently connected to."""
        return self._host

    def new_connection(self, host=None, port=None, timeout=45):
        """Close the current connection (if any) and establish a new one.
        Parameters
        ----------
        See http.client.HTTPSConnection for documentation of the
        parameters. Renew the connection (i.e., reuse the current host
        and port) if host is None or empty.
        Raises
        ------
        DDGConnectionError
        """
        if self._conn:
            self._conn.close()

        if not host:
            host = self._host
            port = self._port
        self._host = host
        self._port = port
        host_display = host + (':%d' % port if port else '')

        proxy = self._proxy
        if proxy:
            logger.debug('Connecting to proxy server %s', proxy)
            self._conn = TLS1_2Connection(proxy, timeout=timeout)

            logger.debug('Tunneling to host %s' % host_display)
            self._conn.set_tunnel(host, port=port)

            try:
                self._conn.connect()
            except Exception as e:
                msg = 'Failed to connect to proxy server %s: %s.' % (proxy, e)
                raise DDGConnectionError(msg)
        else:
            logger.debug('Connecting to new host %s', host_display)
            self._conn = TLS1_2Connection(host, port=port, timeout=timeout)
            try:
                self._conn.connect()
            except Exception as e:
                msg = 'Failed to connect to %s: %s.' % (host_display, e)
                raise DDGConnectionError(msg)

    def renew_connection(self, timeout=45):
        """Renew current connection.
        Equivalent to ``new_connection(timeout=timeout)``.
        """
        self.new_connection(timeout=timeout)

    def fetch_page(self, url):
        """Fetch a URL.
        Allows one reconnection and multiple redirections before failing
        and raising DDGConnectionError.
        Parameters
        ----------
        url : str
            The URL to fetch, relative to the host.
        Raises
        ------
        DDGConnectionError
            When not getting HTTP 200 even after the allowed one
            reconnection and/or one redirection, or when DuckDuckGo is
            blocking query due to unusual activity.
        Returns
        -------
        str
            Response payload, gunzipped (if applicable) and decoded (in UTF-8).
        """
        try:
            self._raw_get(url)
        except (http.client.HTTPException, OSError) as e:
            logger.debug('Got exception: %s.', e)
            logger.debug('Attempting to reconnect...')
            self.renew_connection()
            try:
                self._raw_get(url)
            except http.client.HTTPException as e:
                logger.debug('Got exception: %s.', e)
                raise DDGConnectionError("Failed to get '%s'." % url)

        resp = self._resp
        redirect_counter = 0
        while resp.status != 200 and redirect_counter < 3:
            if resp.status in {301, 302, 303, 307, 308}:
                redirection_url = resp.getheader('location', '')
                if 'sorry/IndexRedirect?' in redirection_url:
                    raise DDGConnectionError('Connection blocked due to unusual activity.')
                self._redirect(redirection_url)
                resp = self._resp
                redirect_counter += 1
            else:
                break

        if resp.status != 200:
            raise DDGConnectionError('Got HTTP %d: %s' % (resp.status, resp.reason))

        payload = resp.read()
        try:
            return gzip.decompress(payload).decode('utf-8')
        except OSError:
            # Not gzipped
            return payload.decode('utf-8')

    def _redirect(self, url):
        """Redirect to and fetch a new URL.
        Like `_raw_get`, the response is stored in ``self._resp``. A new
        connection is made if redirecting to a different host.
        Parameters
        ----------
        url : str
            If absolute and points to a different host, make a new
            connection.
        Raises
        ------
        DDGConnectionError
        """
        logger.debug('Redirecting to URL %s', url)
        segments = urllib.parse.urlparse(url)

        host = segments.netloc
        if host != self._host:
            self.new_connection(host)

        relurl = urllib.parse.urlunparse(('', '') + segments[2:])
        try:
            self._raw_get(relurl)
        except http.client.HTTPException as e:
            logger.debug('Got exception: %s.', e)
            raise DDGConnectionError("Failed to get '%s'." % url)

    def _raw_get(self, url):
        """Make a raw HTTP GET request.
        No status check (which implies no redirection). Response can be
        accessed from ``self._resp``.
        Parameters
        ----------
        url : str
            URL relative to the host, used in the GET request.
        Raises
        ------
        http.client.HTTPException
        """
        logger.debug('Fetching URL %s', url)
        self._conn.request('GET', url, None, {
            'Accept-Encoding': 'gzip',
            'User-Agent': USER_AGENT,
            'Cookie': self.cookie,
            'Connection': 'keep-alive',
            'DNT': '1',
        })
        self._resp = self._conn.getresponse()
        if self.cookie == '':
            complete_cookie = self._resp.getheader('Set-Cookie')
            # Cookie won't be available is already blocked
            if complete_cookie is not None:
                self.cookie = complete_cookie[:complete_cookie.find(';')]
                logger.debug('Cookie: %s' % self.cookie)

    def close(self):
        """Close the connection (if one is active)."""
        if self._conn:
            self._conn.close()


def annotate_tag(annotated_starttag_handler):
    # See parser logic within the DdgParser class for documentation.
    #
    # annotated_starttag_handler(self, tag: str, attrsdict: dict) -> annotation
    # Returns: HTMLParser.handle_starttag(self, tag: str, attrs: list) -> None

    def handler(self, tag, attrs):
        attrs = dict(attrs)
        annotation = annotated_starttag_handler(self, tag, attrs)
        self.insert_annotation(tag, annotation)

    return handler


def retrieve_tag_annotation(annotated_endtag_handler):
    # See parser logic within the DdgParser class for documentation.
    #
    # annotated_endtag_handler(self, tag: str, annotation) -> None
    # Returns: HTMLParser.handle_endtag(self, tag: str) -> None

    def handler(self, tag):
        try:
            annotation = self.tag_annotations[tag].pop()
        except IndexError:
            # Malformed HTML -- more close tags than open tags
            annotation = None
        annotated_endtag_handler(self, tag, annotation)

    return handler


class DdgParser(html.parser.HTMLParser):
    """The members of this class parse the result HTML
    page fetched from DuckDuckGo server for a query.
    The custom parser looks for tags enclosing search
    results and extracts the URL, title and text for
    each search result.
    After parsing the complete HTML page results are
    returned in a list of objects of class Result.
    """

    # Parser logic:
    #
    # - Guiding principles:
    #
    #   1. Tag handlers are contextual;
    #
    #   2. Contextual starttag and endtag handlers should come in pairs
    #      and have a clear hierarchy;
    #
    #   3. starttag handlers should only yield control to a pair of
    #      child handlers (that is, one level down the hierachy), and
    #      correspondingly, endtag handlers should only return control
    #      to the parent (that is, the pair of handlers that gave it
    #      control in the first place).
    #
    #   Principle 3 is meant to enforce a (possibly implicit) stack
    #   structure and thus prevent careless jumps that result in what's
    #   essentially spaghetti code with liberal use of GOTOs.
    #
    # - HTMLParser.handle_endtag gives us a bare tag name without
    #   context, which is not good for enforcing principle 3 when we
    #   have, say, nested div tags.
    #
    #   In order to precisely identify the matching opening tag, we
    #   maintain a stack for each tag name with *annotations*. Important
    #   opening tags (e.g., the ones where child handlers are
    #   registered) can be annotated so that when we can watch for the
    #   annotation in the endtag handler, and when the appropriate
    #   annotation is popped, we perform the corresponding action (e.g.,
    #   switch back to old handlers).
    #
    #   To facilitate this, each starttag handler is decorated with
    #   @annotate_tag, which accepts a return value that is the
    #   annotation (None by default), and additionally converts attrs to
    #   a dict, which is much easier to work with; and each endtag
    #   handler is decorated with @retrieve_tag_annotation which sends
    #   an additional parameter that is the retrieved annotation to the
    #   handler.
    #
    #   Note that some of our tag annotation stacks leak over time: this
    #   happens to tags like <img> and <hr> which are not
    #   closed. However, these tags play no structural role, and come
    #   only in small quantities, so it's not really a problem.
    #
    # - All textual data (result title, result abstract, etc.) are
    #   processed through a set of shared handlers. These handlers store
    #   text in a shared buffer self.textbuf which can be retrieved and
    #   cleared at appropriate times.
    #
    #   Data (including charrefs and entityrefs) are ignored initially,
    #   and when data needs to be recorded, the start_populating_textbuf
    #   method is called to register the appropriate data, charref and
    #   entityref handlers so that they append to self.textbuf. When
    #   recording ends, pop_textbuf should be called to extract the text
    #   and clear the buffer. stop_populating_textbuf returns the
    #   handlers to their pristine state (ignoring data).
    #
    #   Methods:
    #   - start_populating_textbuf(self, data_transformer: Callable[[str], str]) -> None
    #   - pop_textbuf(self) -> str
    #   - stop_populating_textbuf(self) -> None
    #
    # - Outermost starttag and endtag handler methods: root_*. The whole
    #   parser starts and ends in this state.
    #
    # - Each result is wrapped in a <div> tag with class "links_main".
    #
    #   <!-- within the scope of root_* -->
    #   <div class="links_main">  <!-- annotate as 'result', hand over to result_* -->
    #   </div>                    <!-- hand back to root_*, register result -->
    #
    # - For each result, the first <h2> tag with class "result__title" contains the
    #   hyperlinked title.
    #
    #   <!-- within the scope of result_* -->
    #   <h2 class="result__title">  <!-- annotate as 'title', hand over to title_* -->
    #   </h2>                       <!-- hand back to result_* -->
    #
    # - Abstracts are within the scope of <div> tag with class "links_main". Links in
    #   abstract are ignored as they are available within <h2> tag.
    #
    #   <!-- within the scope of result_* -->
    #   <a class="result__snippet">  <!-- annotate as 'abstract', hand over to abstract_* -->
    #   </a>                         <!-- hand back to result_* -->
    #
    # - Each title looks like
    #
    #   <h2 class="result__title">
    #     <!-- within the scope of title_* -->
    #     <a href="result url">  <!-- register self.url, annotate as 'title_link',
    #                                 start_populating_textbuf -->
    #       result title
    #       <span>               <!-- filetype (optional), annotate as title_filetype,
    #                                 start_populating_textbuf -->
    #         file type (e.g. [PDF])
    #       </span>              <!-- stop_populating_textbuf, update self.filetype,
    #                                 start_populating_tetbuf -->
    #     </a>                   <!-- stop_populating_textbuf, pop to self.title
    #                                 prepend self.filetype, if available -->
    #   </h2>

    def __init__(self):
        html.parser.HTMLParser.__init__(self)

        self.filtered = False
        self.results = []

        self.index = 0
        self.textbuf = ''
        self.tag_annotations = {}

        self.set_handlers_to('root')

    ### Tag handlers ###

    @annotate_tag
    def root_start(self, tag, attrs):
        if tag == 'div' and 'links_main' in self.classes(attrs):
            # Initialize result field registers
            self.title = ''
            self.url = ''
            self.abstract = ''
            self.filetype = ''

            self.set_handlers_to('result')
            return 'result'

        # Omitted results
        if tag == 'p' and attrs.get('id') == 'ofr':
            self.filtered = True

    @retrieve_tag_annotation
    def root_end(self, tag, annotation):
        pass

    @annotate_tag
    def result_start(self, tag, attrs):
        if tag == 'h2' and 'result__title' in self.classes(attrs):
            self.set_handlers_to('title')
            return 'title'

        if tag == 'a' and 'result__snippet' in self.classes(attrs) and 'href' in attrs:
            self.start_populating_textbuf()
            return 'abstract'

    @retrieve_tag_annotation
    def result_end(self, tag, annotation):
        if annotation == 'abstract':
            self.stop_populating_textbuf()
            self.abstract = self.pop_textbuf()
        elif annotation == 'result':
            if self.url:
                self.index += 1
                result = Result(self.index, self.title, self.url, self.abstract)
                self.results.append(result)
            self.set_handlers_to('root')

    @annotate_tag
    def title_start(self, tag, attrs):
        if tag == 'span':
            # Print a space after the filetype indicator
            self.start_populating_textbuf(lambda text: '[' + text + ']')
            return 'title_filetype'
        if tag == 'a' and 'href' in attrs:
            # Skip 'News for', 'Images for' search links
            if attrs['href'].startswith('/search'):
                return

            self.url = attrs['href']
            try:
                start = self.url.index('?q=') + len('?q=')
                end = self.url.index('&sa=', start)
                self.url = urllib.parse.unquote_plus(self.url[start:end])
            except ValueError:
                pass
            self.start_populating_textbuf()
            return 'title_link'

    @retrieve_tag_annotation
    def title_end(self, tag, annotation):
        if annotation == 'title_filetype':
            self.stop_populating_textbuf()
            self.filetype = self.pop_textbuf()
            self.start_populating_textbuf()
        elif annotation == 'title_link':
            self.stop_populating_textbuf()
            self.title = self.pop_textbuf()
            if self.filetype != '':
                self.title = self.filetype + self.title
        elif annotation == 'title':
            self.set_handlers_to('result')

    @annotate_tag
    def abstract_start(self, tag, attrs):
        if tag == 'span' and 'st' in self.classes(attrs):
            self.start_populating_textbuf()
            return 'abstract_text'

    @retrieve_tag_annotation
    def abstract_end(self, tag, annotation):
        if annotation == 'abstract_text':
            self.stop_populating_textbuf()
            self.abstract = self.pop_textbuf()
        elif annotation == 'abstract':
            self.set_handlers_to('result')

    ### Generic methods ###

    # Set handle_starttag to SCOPE_start, and handle_endtag to SCOPE_end.
    def set_handlers_to(self, scope):
        self.handle_starttag = getattr(self, scope + '_start')
        self.handle_endtag = getattr(self, scope + '_end')

    def insert_annotation(self, tag, annotation):
        if tag not in self.tag_annotations:
            self.tag_annotations[tag] = []
        self.tag_annotations[tag].append(annotation)

    def start_populating_textbuf(self, data_transformer=None):
        if data_transformer is None:
            # Record data verbatim
            self.handle_data = self.record_data
        else:
            def record_transformed_data(data):
                self.textbuf += data_transformer(data)

            self.handle_data = record_transformed_data

        self.handle_entityref = self.record_entityref
        self.handle_charref = self.record_charref

    def pop_textbuf(self):
        text = self.textbuf
        self.textbuf = ''
        return text

    def stop_populating_textbuf(self):
        self.handle_data = lambda data: None
        self.handle_entityref = lambda ref: None
        self.handle_charref = lambda ref: None

    def record_data(self, data):
        self.textbuf += data

    def record_entityref(self, ref):
        try:
            self.textbuf += chr(html.entities.name2codepoint[ref])
        except KeyError:
            # Entity name not found; most likely rather sloppy HTML
            # where a literal ampersand is not escaped; For instance,
            # containing the following tag
            #
            #     <p class="_e4b"><a href="...">expected market return s&p 500</a></p>
            #
            # where &p is interpreted by HTMLParser as an entity (this
            # behaviour seems to be specific to Python 2.7).
            self.textbuf += '&' + ref

    def record_charref(self, ref):
        if ref.startswith('x'):
            char = chr(int(ref[1:], 16))
        else:
            char = chr(int(ref))
        self.textbuf += char

    @staticmethod
    def classes(attrs):
        """Get tag's classes from its attribute dict."""
        return attrs.get('class', '').split()


Colors = collections.namedtuple('Colors', 'index, title, url, metadata, abstract, prompt, reset')


class Result(object):
    """
    Container for one search result, with output helpers.
    Parameters
    ----------
    index : int or str
    title : str
    url : str
    abstract : str
    Attributes
    ----------
    index : str
    title : str
    url : str
    abstract : str
    Class Variables
    ---------------
    colors : str
    Methods
    -------
    print()
    jsonizable_object()
    urltable()
    """

    # Class variables
    colors = None

    def __init__(self, index, title, url, abstract):
        index = str(index)
        self.title = title
        self.url = url
        self.abstract = abstract

        self._urltable = {index: url}
        subindex = 'a'

    def _print_title_and_url(self, title, url, indent=0):
        colors = self.colors

        # Pad index and url with `indent` number of spaces
        url = ' ' * indent + url
        if colors:
            print(' ' + colors.title + title + colors.reset)
            print(colors.url + url + colors.reset)
        else:
            print(' %s\n%s' % (title, url))

    def _print_abstract(self, abstract, indent=0):
        colors = self.colors
        try:
            columns, _ = os.get_terminal_size()
        except OSError:
            columns = 0

        if colors:
            print(colors.abstract, end='')
        if columns > indent + 1:
            # Try to fill to columns
            fillwidth = columns - indent - 1
            for line in textwrap.wrap(abstract.replace('\n', ''), width=fillwidth):
                print('%s%s' % (' ' * indent, line))
            print('')
        else:
            print('%s\n' % abstract.replace('\n', ' '))
        if colors:
            print(colors.reset, end='')

    def print(self):
        """Print the result entry."""
        self._print_title_and_url(self.title, self.url)
        self._print_abstract(self.abstract)

    def jsonizable_object(self):
        """Return a JSON-serializable dict representing the result entry."""
        obj = {
            'title': self.title,
            'url': self.url,
            'abstract': self.abstract
        }
        return obj

    def urltable(self):
        """Return a index-to-URL table for the current result.
        Normally, the table contains only a single entry, but when the result
        contains sitelinks, all sitelinks are included in this table.
        Returns
        -------
        dict
            A dict mapping indices (strs) to URLs (also strs).
        """
        return self._urltable


class DdgCmdException(Exception):
    pass


class NoKeywordsException(DdgCmdException):
    pass


def require_keywords(method):
    # Require keywords to be set before we run a DdgCmd method. If
    # no keywords have been set, raise a NoKeywordsException.
    @functools.wraps(method)
    def enforced_method(self, *args, **kwargs):
        if not self.keywords:
            raise NoKeywordsException('No keywords.')
        method(self, *args, **kwargs)

    return enforced_method


def no_argument(method):
    # Normalize a do_* method of DdgCmd that takes no argument to
    # one that takes an arg, but issue a warning when an nonempty
    # argument is given.
    @functools.wraps(method)
    def enforced_method(self, arg):
        if arg:
            method_name = arg.__name__
            command_name = method_name[3:] if method_name.startswith('do_') else method_name
            logger.warning("Argument to the '%s' command ignored.", command_name)
        method(self)

    return enforced_method


class DdgCmd(object):
    """
    Command line interpreter and executor class for Ducker.
    Inspired by PSL cmd.Cmd.
    Parameters
    ----------
    opts : argparse.Namespace
        Options and/or arguments.
    Attributes
    ----------
    options : argparse.Namespace
        Options that are currently in effect. Read-only attribute.
    keywords : str or list or strs
        Current keywords. Read-only attribute
    Methods
    -------
    fetch()
    display_results(prelude='\n', json_output=False)
    fetch_and_display(prelude='\n', json_output=False, interactive=True)
    read_next_command()
    help()
    cmdloop()
    """

    # Class variables
    colors = None

    def __init__(self, opts):
        super().__init__()

        self._opts = opts

        self._ddg_url = DdgUrl(opts)
        proxy = opts.proxy if hasattr(opts, 'proxy') else None
        self._conn = DdgConnection(self._ddg_url.hostname, proxy=proxy)
        atexit.register(self._conn.close)

        self.results = []
        self._results_filtered = False
        self._urltable = {}

    @property
    def options(self):
        """Current options."""
        return self._opts

    @property
    def keywords(self):
        """Current keywords."""
        return self._ddg_url.keywords

    @require_keywords
    def fetch(self):
        """Fetch a page and parse for results.
        Results are stored in ``self.results``.
        Raises
        ------
        DDGConnectionError
        See Also
        --------
        fetch_and_display
        """
        # This method also sets self._results_filtered and
        # self._urltable.
        page = self._conn.fetch_page(self._ddg_url.relative())

        if logger.isEnabledFor(logging.DEBUG):
            import tempfile
            fd, tmpfile = tempfile.mkstemp(prefix='Ducker-response-')
            os.close(fd)
            with open(tmpfile, 'w', encoding='utf-8') as fp:
                fp.write(page)
            logger.debug("Response body written to '%s'.", tmpfile)

        parser = DdgParser()
        parser.feed(page)

        self.results = parser.results
        self._results_filtered = parser.filtered
        self._urltable = {}
        for r in self.results:
            self._urltable.update(r.urltable())

    @require_keywords
    def display_results(self, prelude='\n', json_output=False):
        """Display results stored in ``self.results``.
        Parameters
        ----------
        See `fetch_and_display`.
        """
        if json_output:
            # JSON output
            import json
            results_object = [r.jsonizable_object() for r in self.results]
            print(json.dumps(results_object, indent=2, sort_keys=True, ensure_ascii=False))
        else:
            # Regular output
            if not self.results:
                print('No results.', file=sys.stderr)
            else:
                sys.stderr.write(prelude)
                first_shown_result = self._ddg_url._start
                last_shown_result = self._ddg_url._start + self._opts.num
                colors = self.colors
                index = self._ddg_url._start + 1
                for r in self.results[first_shown_result:last_shown_result]:
                    if colors:
                        print(colors.index + str(index) + colors.reset, end='')
                    else:
                        print(str(index), end='')
                    r.print()
                    index += 1

    @require_keywords
    def fetch_and_display(self, prelude='\n', json_output=False, interactive=True):
        """Fetch a page and display results.
        Results are stored in ``self.results``.
        Parameters
        ----------
        prelude : str, optional
            A string that is written to stderr before showing actual results,
            usually serving as a separator. Default is an empty line.
        json_output : bool, optional
            Whether to dump results in JSON format. Default is False.
        interactive : bool, optional
            Whether to show contextual instructions, when e.g. DuckDuckGo
            has filtered the results. Default is True.
        Raises
        ------
        DDGConnectionError
        See Also
        --------
        fetch
        display_results
        """
        self.fetch()
        self.display_results(prelude=prelude, json_output=json_output)
        if self._results_filtered:
            printerr('** Enter "unfilter" to show similar results DuckDuckGo omitted.')

    def read_next_command(self):
        """Show omniprompt and read user command line.
        Command line is always stripped, and each consecutive group of
        whitespace is replaced with a single space character. If the
        command line is empty after stripping, when ignore it and keep
        reading. Exit with status 0 if we get EOF or an empty line
        (pre-strip, that is, a raw <enter>) twice in a row.
        The new command line (non-empty) is stored in ``self.cmd``.
        """
        colors = self.colors
        message = 'Ducker (? for help)'
        prompt = (colors.prompt + message + colors.reset + ' ') if colors else (message + ': ')
        enter_count = 0
        while True:
            try:
                cmd = input(prompt)
            except EOFError:
                sys.exit(0)

            if not cmd:
                enter_count += 1
                if enter_count == 2:
                    # Double <enter>
                    sys.exit(0)
            else:
                enter_count = 0

            cmd = ' '.join(cmd.split())
            if cmd:
                self.cmd = cmd
                break

    @staticmethod
    def help():
        DdgArgumentParser.print_omniprompt_help(sys.stderr)
        printerr('')

    @require_keywords
    @no_argument
    def do_first(self):
        self._ddg_url.first_page()
        self.fetch_and_display()

    def do_ddg(self, arg):
        # Update keywords and reconstruct URL
        self._opts.keywords = arg
        self._ddg_url = DdgUrl(self._opts)
        # If there is a Bang, let DuckDuckGo do the work
        if arg[0] == '!':
            webbrowser.open(self._ddg_url.full())
        else:
            self.fetch_and_display()

    @require_keywords
    @no_argument
    def do_next(self):
        # If > 5 results are being fetched each time,
        # block next when no parsed results in current fetch
        if not self.results and self._ddg_url._num > 5:
            printerr('No results.')
        else:
            self._ddg_url.next_page()
            self.fetch_and_display()

    @require_keywords
    def do_open(self, *args):
        if not args:
            open_url(self._ddg_url.full())
            return

        for nav in args:
            if nav in self._urltable:
                open_url(self._urltable[nav])
            else:
                printerr('Invalid index %s.' % nav)

    @require_keywords
    @no_argument
    def do_previous(self):
        try:
            self._ddg_url.prev_page()
        except ValueError as e:
            print(e, file=sys.stderr)
            return

        self.fetch_and_display()

    @require_keywords
    @no_argument
    def do_unfilter(self):
        # Reset start to 0 when unfilter is applied.
        self._ddg_url.update(None, **{'start':0,})
        self._ddg_url.set_queries(filter=0)
        self.fetch_and_display()

    def cmdloop(self):
        """Run REPL."""
        if self.keywords:
            self.fetch_and_display()
        else:
            printerr('Please initiate a query.')

        while True:
            self.read_next_command()
            # TODO: Automatic dispatcher
            #
            # We can't write a dispatcher for now because that could
            # change behaviour of the prompt. However, we have already
            # laid a lot of ground work for the dispatcher, e.g., the
            # `no_argument' decorator.
            try:
                cmd = self.cmd
                if cmd == 'f':
                    self.do_first('')
                elif cmd.startswith('g '):
                    self.do_ddg(cmd[2:])
                elif cmd == 'n':
                    self.do_next('')
                elif cmd == 'o':
                    self.do_open()
                elif cmd.startswith('o '):
                    self.do_open(*cmd[2:].split())
                elif cmd == 'p':
                    self.do_previous('')
                elif cmd == 'q':
                    break
                elif cmd == 'unfilter':
                    self.do_unfilter('')
                elif cmd == '?':
                    self.help()
                elif cmd in self._urltable:
                    open_url(self._urltable[cmd])
                elif self.keywords and cmd.isdigit() and int(cmd) < 100:
                    printerr('Index out of bound. To search for the number, use g.')
                else:
                    self.do_ddg(cmd)
            except NoKeywordsException:
                printerr('Initiate a query first.')


class DdgArgumentParser(argparse.ArgumentParser):
    """Custom argument parser for Ducker."""

    # Print omniprompt help
    @staticmethod
    def print_omniprompt_help(file=None):
        file = sys.stderr if file is None else file
        file.write(textwrap.dedent("""
        omniprompt keys:
          n, p                  fetch the next or previous set of search results
          index                 open the result corresponding to index in browser
          f                     jump to the first page
          o [index ...]         open space-separated result indices in browser
                                open the current search in browser, if no arguments
          g keywords            fire a new search for 'keywords' with original options
          q, ^D, double Enter   exit
          ?                     show omniprompt help
          *                     any other string fires a new search with original options
        """))

    # Print information on Ducker
    @staticmethod
    def print_general_info(file=None):
        file = sys.stderr if file is None else file
        file.write(textwrap.dedent("""
        Version %s
        Copyright (C) 2016 Arun Prakash Jana <engineerarun@gmail.com>
        Copyright (C) 2016-2017 Jorge Maldonado Ventura <jorgesumle@freakspot.net>
        License: GPLv3
        Webpage: http://programas.freakspot.net/ducker/
        """ % __version__))

    # Augment print_help to print more than synopsis and options
    def print_help(self, file=None):
        super().print_help(file)
        self.print_omniprompt_help(file)
        self.print_general_info(file)

    # Automatically print full help text on error
    def error(self, message):
        sys.stderr.write('%s: error: %s\n\n' % (self.prog, message))
        self.print_help(sys.stderr)
        self.exit(2)

    # Type guards
    @staticmethod
    def positive_int(arg):
        """Try to convert a string into a positive integer."""
        try:
            n = int(arg)
            assert n > 0
            return n
        except (ValueError, AssertionError):
            raise argparse.ArgumentTypeError('%s is not a positive integer' % arg)

    @staticmethod
    def nonnegative_int(arg):
        """Try to convert a string into a nonnegative integer."""
        try:
            n = int(arg)
            assert n >= 0
            return n
        except (ValueError, AssertionError):
            raise argparse.ArgumentTypeError('%s is not a non-negative integer' % arg)

    @staticmethod
    def is_duration(arg):
        """Check if a string is a valid duration accepted by DuckDuckGo.
        A valid duration is d (past day), w (past week), m (past month) or a
        (any time).
        """
        try:
            if arg not in ('d', 'w', 'm', 'a'):
                raise ValueError
        except (TypeError, IndexError, ValueError):
            raise argparse.ArgumentTypeError('%s is not a valid duration' % arg)
        return arg

    @staticmethod
    def is_colorstr(arg):
        """Check if a string is a valid color string."""
        try:
            assert len(arg) == 6
            for c in arg:
                assert c in COLORMAP
        except AssertionError:
            raise argparse.ArgumentTypeError('%s is not a valid color string' % arg)
        return arg


def parse_args(args=None, namespace=None):
    """Parse Ducker arguments/options.
    Parameters
    ----------
    args : list, optional
        Arguments to parse. Default is ``sys.argv``.
    namespace : argparse.Namespace
        Namespace to write to. Default is a new namespace.
    Returns
    -------
    argparse.Namespace
        Namespace with parsed arguments / options.
    """

    colorstr_env = os.getenv('DDGR_COLORS')

    argparser = DdgArgumentParser(description='DuckDuckGo from the command-line.',
                                  prog='Ducker')

    addarg = argparser.add_argument

    # First display -h, --help and --version
    addarg('--version', action='version', version='%(prog)s ' + __version__,
           help='output version information and exit')

    addarg('-m', '--multiple-search', action='store_true',
           help='launch a search for every word given')

    # Search categories
    addarg('-i', '--image-search', action='store_true',
           help='search for images')
    addarg('-v', '--video-search', action='store_true',
           help='search for videos')
    addarg('-w', '--website-search', action='store_true',
           help='search for websites')

    addarg('-H', '--no-javascript', action='store_true',
           help='search with DuckDuckGo html interface')
    addarg('-l', '--lite', action='store_true',
           help='search with DuckDuckGo lite interface.')

    # Positional arguments
    addarg('keywords', nargs='*', metavar='KEYWORD',
           help='search keywords')

    # Interactive mode
    addarg('-s', '--start', dest='start', type=argparser.nonnegative_int,
           default=0, metavar='N',
           help='start at the Nth result')
    addarg('-n', '--count', dest='num', type=argparser.positive_int,
           default=8, metavar='N',
           help='show N results (default 8)')
    addarg('-c', '--reg', dest='reg', metavar='REG',
           help="region-specific search e.g. 'in-en' for India; visit https://duckduckgo.com/params")
    addarg('-x', '--exact', dest='exact', action='store_true',
           help='disable automatic spelling correction')
    addarg('-C', '--nocolor', dest='colorize', action='store_false',
           help='disable color output')
    addarg('--colors', dest='colorstr', type=argparser.is_colorstr,
           default=colorstr_env if colorstr_env else 'GKlgxy', metavar='COLORS',
           help='set output colors (see man page for details)')
    addarg('-t', '--time', dest='duration', type=argparser.is_duration,
           help='time limit search '
           '[a (any time), d (past day), w (past week), m (past month)]')
    addarg('--site', dest='site', metavar='SITE',
           help='search a site using DuckDuckGo')
    addarg('-p', '--proxy', dest='proxy',
           help='tunnel traffic through an HTTPS proxy (HOST:PORT)')
    addarg('--noua', dest='noua', action='store_true',
           help='disable user agent')
    addarg('--json', dest='json', action='store_true',
           help='output in JSON format; implies --noprompt')
    addarg('--np', '--noprompt', dest='noninteractive', action='store_true',
           help='perform search and exit, do not prompt')
    addarg('-d', '--debug', dest='debug', action='store_true',
           help='enable debugging')

    return argparser.parse_args(args, namespace)


def build_search_url(search_str, args):
    """Build the search URL with the suplied search string and arguments."""

    base_url = 'https://duckduckgo.com/'

    if args.exact:
        search_str = '"' + search_str + '"'

    if args.site:
        query_string = 'q=site:{} {}'.format(args.site, search_str)
    else:
        query_string = 'q=' + search_str

    if args.no_javascript:
        base_url += 'html/'
    elif args.lite:
        base_url += 'lite/'
    # Image and video modes are only avalible in the JavaScript version of DuckDuckGo.
    else:
        if args.website_search:
            query_string += '&ia=web'
        elif args.image_search:
            query_string += '&ia=images'
        elif args.video_search:
            query_string += '&ia=videos'

    if args.reg:
        query_string += '&kl=' + args.reg

    if args.duration:
        query_string += '&df=' + args.duration

    return '{}?{}'.format(base_url, query_string)


def open_url(url):
    """Open an URL in the user's default web browser.
    Whether the browser's output (both stdout and stderr) are suppressed
    depends on the boolean attribute ``open_url.suppress_browser_output``.
    If the attribute is not set upon a call, set it to a default value,
    which means False if BROWSER is set to a known text-based browser --
    elinks, links, lynx or w3m; or True otherwise.
    """
    if not hasattr(open_url, 'suppress_browser_output'):
        open_url.suppress_browser_output = (os.getenv('BROWSER') not in
                                            ['elinks', 'links', 'lynx', 'w3m'])
    logger.debug('Opening %s', url)
    if open_url.suppress_browser_output:
        _stderr = os.dup(2)
        os.close(2)
        _stdout = os.dup(1)
        os.close(1)
        fd = os.open(os.devnull, os.O_RDWR)
        os.dup2(fd, 2)
        os.dup2(fd, 1)
    try:
        webbrowser.open(url)
    finally:
        if open_url.suppress_browser_output:
            os.close(fd)
            os.dup2(_stderr, 2)
            os.dup2(_stdout, 1)


def repl(opts):
    try:
        global USER_AGENT

        # Set colors
        if opts.colorize:
            colors = Colors(*[COLORMAP[c] for c in opts.colorstr], reset=COLORMAP['x'])
        else:
            colors = None
        Result.colors = colors
        DdgCmd.colors = colors

        if opts.noua:
            USER_AGENT = ''

        repl = DdgCmd(opts)

        if opts.json or opts.noninteractive:
            # Non-interactive mode
            repl.fetch()
            repl.display_results(prelude='', json_output=opts.json)
            sys.exit(0)
        else:
            # Interactive mode
            repl.cmdloop()
    except Exception as e:
        # If debugging mode is enabled, let the exception through for a traceback;
        # otherwise, only print the exception error message.
        if logger.isEnabledFor(logging.DEBUG):
            raise
        else:
            logger.error(e)
            sys.exit(1)

def make_searches():
    """Make the searches specified by the user."""
    args = parse_args()

    # Set logging level
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Version %s', __version__)

    if args.multiple_search:
        for keyword in args.keywords:
            search_url = build_search_url(keyword, args)
            open_url(search_url)
    elif len(args.keywords) == 0 or args.noninteractive or args.json:
        repl(args)
    else:
        search_url = build_search_url(' '.join(args.keywords), args)
        open_url(search_url)
