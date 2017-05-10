import threading

from wsgiref.simple_server import make_server

from .test_wsgiprox import BaseWSGIProx, scheme, ws_scheme


# ============================================================================
class Test_wsgiref_WSGIProx(BaseWSGIProx):
    @classmethod
    def setup_class(cls):
        super(Test_wsgiref_WSGIProx, cls).setup_class()

        cls.server = make_server('', 0, cls.app)

        cls.port = cls.server.socket.getsockname()[1]

        cls.proxies = cls.proxy_dict(cls.port)

        def run():
            cls.server.serve_forever()

        cls.server_type = 'wsgiref'

        cls.thread = threading.Thread(target=run)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def teardown_class(cls):
        super(Test_wsgiref_WSGIProx, cls).teardown_class()
        cls.server.shutdown()


