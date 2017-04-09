# -*- coding: utf-8 -*-
"""
    pip_services_net.rest.RestService
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    REST service implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import bottle
import json
import time

from threading import Thread

from pip_services_commons.config import IConfigurable, ConfigParams
from pip_services_commons.refer import IReferenceable, DependencyResolver
from pip_services_commons.run import IOpenable, IClosable
from pip_services_commons.connect import ConnectionParams, ConnectionResolver
from pip_services_commons.log import CompositeLogger
from pip_services_commons.count import CompositeCounters
from pip_services_commons.errors import ConfigException, ConnectionException
from pip_services_commons.errors import ErrorDescription, ErrorDescriptionFactory
from pip_services_commons.data import FilterParams, PagingParams

from .SimpleServer import SimpleServer

class RestService(object, IOpenable, IClosable, IConfigurable, IReferenceable):
    _default_config = ConfigParams.from_tuples(
        "connection.protocol", "http",
        "connection.host", "0.0.0.0",
        #"connection.port", 3000,
        "connection.request_max_size", 1024 * 1024,
        "connection.connect_timeout", 60000,
        "connection.debug", False
    )

    _service = None
    _server = None
    _debug = False
    _connection_resolver = None
    _dependency_resolver = None
    _logger = None
    _counters = None
    _uri = None
    _registered = None


    def __init__(self):
        self._registered = False
        self._connection_resolver = ConnectionResolver()
        self._dependency_resolver = DependencyResolver()
        self._logger = CompositeLogger()
        self._counters = CompositeCounters()

        # Create instance of bottle application
        self._service = bottle.Bottle(catchall=True, autojson=True)
        
        # Enable CORS requests
        self._service.add_hook('after_request', self._enable_cors)
        self._service.route('/', 'OPTIONS', self._options_handler)
        self._service.route('/<path:path>', 'OPTIONS', self._options_handler)


    def _enable_cors(self):
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        bottle.response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

    def _options_handler(self, ath = None):
        return

    def _instrument(self, correlation_id, name):
        self._logger.trace(correlation_id, "Executing " + name + " method")
        return self._counters.begin_timing(name + ".exec_time")


    def set_references(self, references):
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._connection_resolver.set_references(references)
        self._dependency_resolver.set_references(references)


    def configure(self, config):
        config = config.set_defaults(self._default_config)
        self._connection_resolver.configure(config)
        self._dependency_resolver.configure(config)


    def _get_connection(self, correlation_id):
        connection = self._connection_resolver.resolve(correlation_id)
        
        # Check for connection
        if connection == None:
            raise ConfigException(correlation_id, "NO_CONNECTION", "Connection for REST client is not defined")
        
        # Check for type
        protocol = connection.get_protocol("http");
        if "http" != protocol:
            raise ConfigException(
                correlation_id, "WRONG_PROTOCOL", "Protocol is not supported by REST connection"
            ).with_details("protocol", protocol)

        # Check for host
        if connection.get_host() == None:
            raise ConfigException(correlation_id, "NO_HOST", "No host is configured in REST connection")

        # Check for port
        if connection.get_port() == 0:
            raise ConfigException(correlation_id, "NO_PORT", "No port is configured in REST connection")
        
        return connection


    def open(self, correlation_id):
        # Register (add) flask routes
        if self._registered != True:
            self.register()
            self._registered = True

        connection = self._get_connection(correlation_id)

        host = connection.get_host()
        port = connection.get_port()
        self._uri = connection.get_uri()
        self._uri = self._uri if self._uri != None else "http://" + str(host) + ":" + str(port)

        def start_server():
            self._service.run(server=self._server, debug=self._debug)

        # Starting service
        try:
            self._server = SimpleServer(host=host, port=port)

            # Start server in thread
            Thread(target=start_server).start()

            # Give 2 sec for initialization
            #time.sleep(2)
            self._logger.info(correlation_id, "Opened REST service at " + self._uri)
        except Exception as ex:
            self._server = None

            raise ConnectionException(correlation_id, 'CANNOT_CONNECT', 'Opening REST service failed') \
                .wrap(ex).with_details('url', self._uri)


    def close(self, correlation_id):
        try:
            if self._server != None:
                self._server.shutdown()
                self._logger.info(correlation_id, "Closed REST service at " + self._uri)

            self._server = None
            self._uri = None
        except Exception as ex:
            self._logger.warn(correlation_id, "Failed while closing REST service: " + str(ex))


    def _to_json(self, obj):
        if obj == None:
            return None

        if isinstance(obj, set):
            obj = list(obj)
        if isinstance(obj, list):
            result = []
            for item in obj:
                item = self._to_json(item)
                result.append(item)
            return result

        if isinstance(obj, dict):
            result = {}
            for (k, v) in obj.items():
                v = self._to_json(v)
                result[k] = v
            return result
        
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        if hasattr(obj, '__dict__'):
            return self._to_json(obj.__dict__)
        return obj


    def send_result(self, result):
        bottle.response.headers['Content-Type'] = 'application/json'
        if result == None: 
            bottle.response.status = 404
            return
        else:
            bottle.response.status = 200
            return json.dumps(result, default=self._to_json)


    def send_created_result(self, result):
        bottle.response.headers['Content-Type'] = 'application/json'
        if result == None: 
            bottle.response.status = 404
            return
        else:
            bottle.response.status = 201
            return json.dumps(result, default=self._to_json)


    def send_deleted_result(self):
        bottle.response.headers['Content-Type'] = 'application/json'
        bottle.response.status = 204
        return


    def send_error(self, error):
        bottle.response.headers['Content-Type'] = 'application/json'
        error = ErrorDescriptionFactory.create(error)
        if error.correlation_id == None:
            error.correlation_id = self.get_correlation_id()
        bottle.response.status = error.status
        return json.dumps(error.to_json())


    def get_param(self, param, default = None):
        return bottle.request.params.get(param, default)


    def get_correlation_id(self):
        return bottle.request.query.get('correlation_id')


    def get_filter_params(self):
        data = dict(bottle.request.query.decode())
        data.pop('correlation_id', None)
        data.pop('skip', None)
        data.pop('take', None)
        data.pop('total', None)
        return FilterParams(data)


    def get_paging_params(self):
        skip = bottle.request.query.get('skip')
        take = bottle.request.query.get('take')
        total = bottle.request.query.get('total')
        return PagingParams(skip, take, total)


    def get_data(self):
        return bottle.request.json


    def register_route(self, method, route, handler):
        method = method.upper()

        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception as ex:
                return self.send_error(ex)

        self._service.route(route, method, wrapper)


    def register(self):
        pass