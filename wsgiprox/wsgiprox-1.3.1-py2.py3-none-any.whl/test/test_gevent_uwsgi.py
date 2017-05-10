from gevent.monkey import patch_all; patch_all(thread=False)
from gevent.pywsgi import WSGIServer
import gevent

from wsgiprox.resolvers import FixedResolver, ProxyAuthResolver
from .test_wsgiprox import BaseWSGIProx, scheme, ws_scheme

import sys
import re
import os
import requests
import websocket
import pytest

import subprocess


# ============================================================================
class WebSocketMixin(object):
    def test_websocket(self, ws_scheme):
        scheme = ws_scheme.replace('ws', 'http')
        pytest.importorskip('geventwebsocket.handler')

        ws = websocket.WebSocket(sslopt={'ca_certs': self.root_ca_file})
        ws.connect('{0}://example.com/websocket?a=b'.format(ws_scheme),
                   http_proxy_host='localhost',
                   http_proxy_port=self.port)

        ws.send('{0} message'.format(ws_scheme))
        msg = ws.recv()
        assert(msg == 'WS Request Url: /prefix/{0}://example.com/websocket?a=b Echo: {1} message'.format(scheme, ws_scheme))

    def test_websocket_fixed_host(self, ws_scheme):
        scheme = ws_scheme.replace('ws', 'http')
        pytest.importorskip('geventwebsocket.handler')

        ws = websocket.WebSocket(sslopt={'ca_certs': self.root_ca_file})
        ws.connect('{0}://wsgiprox/websocket?a=b'.format(ws_scheme),
                   http_proxy_host='localhost',
                   http_proxy_port=self.port)

        ws.send('{0} message'.format(ws_scheme))
        msg = ws.recv()
        assert(msg == 'WS Request Url: /websocket?a=b Echo: {1} message'.format(scheme, ws_scheme))

    def test_error_websocket_ignored(self, ws_scheme):
        scheme = ws_scheme.replace('ws', 'http')
        pytest.importorskip('geventwebsocket.handler')

        ws = websocket.WebSocket(sslopt={'ca_certs': self.root_ca_file})
        ws.connect('{0}://wsgiprox/websocket?ignore_ws=true'.format(ws_scheme),
                   http_proxy_host='localhost',
                   http_proxy_port=self.port)

        ws.send('{0} message'.format(ws_scheme))
        ws.settimeout(0.2)
        with pytest.raises(Exception):
            msg = ws.recv()


# ============================================================================
class Test_gevent_WSGIProx(BaseWSGIProx, WebSocketMixin):
    @classmethod
    def setup_class(cls):
        super(Test_gevent_WSGIProx, cls).setup_class()
        cls.server = WSGIServer(('localhost', 0), cls.app)
        cls.server.init_socket()
        cls.port = str(cls.server.address[1])

        gevent.spawn(cls.server.serve_forever)

        cls.proxies = cls.proxy_dict(cls.port)

        cls.auth_resolver = ProxyAuthResolver()

        cls.server_type = 'gevent'

    def _test_proxy_auth_required(self, scheme):
        self.app.prefix_resolver = self.auth_resolver

        with pytest.raises(requests.exceptions.RequestException) as err:
            res = requests.get('{0}://example.com/path/file?foo=bar'.format(scheme),
                               proxies=self.proxies)

            res.raise_for_status()

        assert '407 ' in str(err.value)

    def _test_proxy_auth_success(self, scheme):
        self.app.prefix_resolver = self.auth_resolver

        proxies = self.proxy_dict(self.port, 'other-prefix:ignore@localhost')

        res = requests.get('{0}://example.com/path/file?foo=bar'.format(scheme),
                           proxies=proxies,
                           verify=self.root_ca_file)

        assert(res.text == 'Requested Url: /other-prefix/{0}://example.com/path/file?foo=bar'.format(scheme))

    def test_error_proxy_unsupported(self):
        from waitress.server import create_server
        server = create_server(self.app, host='127.0.0.1', port=0)

        port = server.effective_port

        gevent.spawn(server.run)

        proxies = self.proxy_dict(port)

        # http proxy not supported: just passes through
        res = requests.get('http://example.com/path/file?foo=bar',
                           proxies=proxies,
                           verify=self.root_ca_file)

        assert(res.text == 'Requested Url: /path/file?foo=bar')

        # https proxy (via CONNECT) not supported
        with pytest.raises(requests.exceptions.ProxyError) as err:
            res = requests.get('https://example.com/path/file?foo=bar',
                               proxies=proxies,
                               verify=self.root_ca_file)

        assert '405 ' in str(err.value)


# ============================================================================
@pytest.mark.skipif(sys.platform == 'win32', reason='no uwsgi on windows')
class Test_uwsgi_WSGIProx(BaseWSGIProx, WebSocketMixin):
    @classmethod
    def setup_class(cls):
        super(Test_uwsgi_WSGIProx, cls).setup_class()

        cls.root_ca_file = os.path.join(cls.test_ca_dir, 'ca', 'wsgiprox-ca.pem')

        env = os.environ.copy()
        env['CA_ROOT_DIR'] = cls.test_ca_dir

        curr_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))

        try:
            cls.uwsgi = subprocess.Popen(['uwsgi', 'uwsgi.ini'], env=env, cwd=curr_dir,
                                         stderr=subprocess.PIPE)

        except Exception as e:
            pytest.skip('uwsgi not found, skipping uwsgi tests')

        port_rx = re.compile('uwsgi socket 0 bound to TCP address :([\d]+)')

        while True:
            line = cls.uwsgi.stderr.readline().decode('utf-8')
            m = port_rx.search(line)
            if m:
                cls.port = int(m.group(1))
                break

        cls.proxies = cls.proxy_dict(cls.port)

        cls.server_type = 'uwsgi'

    @classmethod
    def teardown_class(cls):
        cls.uwsgi.terminate()
        super(Test_uwsgi_WSGIProx, cls).teardown_class()


