import pytest
from bottle import Bottle, ServerAdapter
from threading import Thread
from schul_cloud_ressources_api_v1.schema import get_valid_examples
import time
import requests

# configuration
NUMBER_OF_VALID_RESSOURCES = 3
STARTUP_TIMEOUT = 2 # seconds

# module constants
VALID_RESSOURCES = get_valid_examples()


@pytest.fixture(scope="session")
def host():
    """The host of the application."""
    return "localhost"


class WSGIRefServer(ServerAdapter):
    # copied from bottle
    def run(self, app): # pragma: no cover
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self): # Prevent reverse DNS lookups please.
                return self.client_address[0]
            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls  = self.options.get('server_class', WSGIServer)

        if ':' in self.host: # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        self.srv = make_server(self.host, 0, app, server_cls, handler_cls)
        self.srv.serve_forever()

    def shutdown(self):
        """Stop the server."""
        self.srv.shutdown()

    def get_port(self):
        """Return the port of the server."""
        try:
            return self.srv.socket.getsockname()[1]
        except AttributeError:
            return None


@pytest.fixture(scope="session")
def _server():
    """The server to start the app."""
    return WSGIRefServer()


@pytest.fixture(scope="session")
def app(_server, host):
    """The bottle app serving the ressources."""
    app = Bottle()
    # app.run http://bottlepy.org/docs/dev/api.html#bottle.run
    thread = Thread(target=app.run, kwargs=dict(host=host, server=_server))
    thread.start()
    while not _server.get_port(): time.sleep(0.001)
    yield app
    # app.close http://bottlepy.org/docs/dev/api.html#bottle.Bottle.close
    app.close()
    _server.shutdown()
    thread.join()


@pytest.fixture
def port(_server, app):
    """The port of the application running."""
    return _server.get_port()


@pytest.fixture
def base_url(host, port):
    """The http url to the server for resources.

    The server is not started.
    """
    return "http://{}:{}".format(host, port)


@pytest.fixture
def serve(app, base_url):
    """A function to serve ressources."""
    served = []
    def serve(body):
        """Serve a response body and return the url."""
        url = "/res/" + str(len(served)) 
        served.append(url)
        app.get(url, callback=lambda: body)
        return base_url + url
    yield serve
    app.reset()


_ressource_id = 0

def ressource_with_id(ressource):
    """Set the id for a ressource."""
    global _ressource_id
    _ressource_id += 1
    ressource = ressource.copy()
    assert "X-Test-Id" not in ressource
    ressource["X-Test-Id"] = _ressource_id
    return ressource

@pytest.fixture(params=VALID_RESSOURCES[:NUMBER_OF_VALID_RESSOURCES])
def ressource(request):
    """A valid ressource."""
    return ressource_with_id(request.param)


@pytest.fixture
def ressource_url(ressource, serve):
    """The url to retrieve the valid ressource."""
    return serve(ressource)


@pytest.fixture(params=[
        VALID_RESSOURCES,       # all valid resssources
        [VALID_RESSOURCES[0]],  # one valid ressource
        VALID_RESSOURCES[::-2], # every second ressource in reversed order
        []                       # no ressources
    ])
def ressources(request):
    """A list of ressources."""
    return list(map(ressource_with_id, request.param))


@pytest.fixture
def ressource_urls(ressources, serve):
    """The list of orls where the ressources can be found."""
    return [serve(ressource) for ressource in ressources]




