import flask
import json
import inspect

from .handle import Resource
from .route import RouteFactory
from .utils import Logger
from .error import RequestError
from .db import TinyBDDatabase, Database


class App(object):
    def __init__(self, base_route, db=None):
        self.base_route = base_route
        self.debug = True

        self.app = flask.Flask(__name__)
        self.route_factory = RouteFactory(base_route)

        self.routes = {}

        self.db = None
        if db is None:
            self.db = TinyBDDatabase('db.json')

        # flask_cors.CORS(self.app)

        self._create_index()

        @self.app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers',
                                 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods',
                                 'GET,PUT,POST,DELETE')
            return response

    def add_resource(self, resource):
        if inspect.isclass(resource) and issubclass(resource, Resource):
            instance = resource(self)
            instance.on_create()
        elif isinstance(resource, str):
            instance = Resource(self, name=resource)
        else:
            raise ValueError(
                'Resource should be a subclass of Resource or a string')

        self.routes[instance.get_name()] = self._inspect_list(instance)[1]

        self._inspect_post(instance)
        self._inspect_get(instance)
        self._inspect_delete(instance)
        self._inspect_put(instance)

        return instance

    def _add_route(self, route, endpoint, as_name, method):
        if inspect.ismethod(endpoint):
            # wrap the instance method to a lambda function, see the comments
            # below for explanation.
            cb = endpoint

            def endpoint(*args, **kwargs):
                return cb(*args, **kwargs)

        def wrapper(*args, **kwargs):
            try:
                return endpoint(*args, **kwargs)
            except RequestError as e:
                return self._response_error(e.status, e.message)

        if as_name is not None:
            # this is done to avoid flask's "View function mapping is
            # overwriting an existing endpoint function: endpoint" error.
            # but it requires that the function is not a an instance method.
            wrapper.__name__ = as_name
        self.app.route(route, methods=[method])(wrapper)
        Logger.debug("Create route for %s: %s", wrapper.__name__, route)
        return wrapper.__name__, route, method

    def _inspect_list(self, instance):
        route = self.route_factory.create_list(instance)
        name = instance.get_name()

        def endpoint():
            return self._response_middleware(instance.list())

        return self._add_route(route, endpoint, '%s_list' % name, 'GET')

    def _inspect_post(self, instance):
        route = self.route_factory.create_post(instance)
        name = instance.get_name()

        def endpoint():
            body = flask.request.get_json()
            return self._response_middleware(instance.post(body))

        return self._add_route(route, endpoint, '%s_post' % name, 'POST')

    def _inspect_get(self, instance):
        route = self.route_factory.create_get(instance)
        name = instance.get_name()

        def endpoint(pk):
            return self._response_middleware(instance.get(int(pk)))

        return self._add_route(route, endpoint, '%s_get' % name, 'GET')

    def _inspect_delete(self, instance):
        route = self.route_factory.create_delete(instance)
        name = instance.get_name()

        def endpoint(pk):
            return self._response_middleware(instance.delete(int(pk)))

        return self._add_route(route, endpoint, '%s_delete' % name, 'DELETE')

    def _inspect_put(self, instance):
        route = self.route_factory.create_delete(instance)
        name = instance.get_name()

        def endpoint(pk):
            body = flask.request.get_json()
            return self._response_middleware(instance.put(int(pk), body))

        return self._add_route(route, endpoint, '%s_put' % name, 'PUT')

    @staticmethod
    def _response_middleware(response):
        return flask.Response(json.dumps(response),
                              mimetype='application/json')

    @staticmethod
    def _response_error(status, message):
        return flask.Response(json.dumps({
            'message': message
        }), mimetype='application/json', status=status)

    def _create_index(self):
        base_route = '/%s/' % self.route_factory.base_route
        self._add_route(base_route, self._index, 'index', 'GET')

    def _index(self):
        return self._response_middleware(self.routes)

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(host=host, port=port, threaded=True)
