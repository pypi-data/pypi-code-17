import flask
import re
import json
import inspect
import flask_cors

from handle import Resource
from route import RouteFactory
from utils import Logger
from error import Error404
from db import UnQLiteQueryObject


class App(object):
    def __init__(self, base_route):
        self.base_route = base_route
        self.debug = True

        self.app = flask.Flask(__name__)
        self.route_factory = RouteFactory(base_route)

        flask_cors.CORS(self.app)

        @self.app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
            return response

    def add_resource(self, resource):
        if inspect.isclass(resource) and issubclass(resource, Resource):
            instance = resource(self)
            instance.on_create()
        elif isinstance(resource, str):
            instance = Resource(self, name=resource)

        self._inspect_list(instance)
        self._inspect_post(instance)
        self._inspect_get(instance)
        self._inspect_delete(instance)
        self._inspect_put(instance)

        return instance

    def _add_route(self, route, endpoint, as_name, method):
        if as_name is not None:
            endpoint.__name__ = as_name
        self.app.route(route, methods=[method])(endpoint)
        Logger.debug("Create route for %s: %s", endpoint.__name__, route)

    def _inspect_list(self, instance):
        route = self.route_factory.create_list(instance)
        name = instance.get_name()

        def endpoint():
            return self._response_middleware(instance.list())

        self._add_route(route, endpoint, '%s_list' % name, 'GET')

    def _inspect_post(self, instance):
        route = self.route_factory.create_post(instance)
        name = instance.get_name()

        def endpoint():
            body = flask.request.get_json()
            return self._response_middleware(instance.post(body))

        self._add_route(route, endpoint, '%s_post' % name, 'POST')

    def _inspect_get(self, instance):
        route = self.route_factory.create_get(instance)
        name = instance.get_name()

        def endpoint(pk):
            try:
                return self._response_middleware(instance.get(long(pk)))
            except Error404:
                return self._response_error(404, 'Object not found')

        self._add_route(route, endpoint, '%s_get' % name, 'GET')

    def _inspect_delete(self, instance):
        route = self.route_factory.create_delete(instance)
        name = instance.get_name()

        def endpoint(pk):
            return self._response_middleware(instance.delete(long(pk)))

        self._add_route(route, endpoint, '%s_delete' % name, 'DELETE')

    def _inspect_put(self, instance):
        route = self.route_factory.create_delete(instance)
        name = instance.get_name()

        def endpoint(pk):
            body = flask.request.get_json()
            return self._response_middleware(instance.put(long(pk), body))

        self._add_route(route, endpoint, '%s_put' % name, 'PUT')

    def _response_middleware(self, response):
        return flask.Response(json.dumps(response), mimetype='application/json')

    def _response_error(self, status, message):
        return flask.Response(json.dumps({
            'message': message
        }), mimetype='application/json', status=404)

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(host=host, port=port, threaded=True)

        UnQLiteQueryObject.db.close()
