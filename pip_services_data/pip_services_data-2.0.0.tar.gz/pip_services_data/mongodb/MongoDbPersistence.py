# -*- coding: utf-8 -*-
"""
    pip_services_data.mongodb.MemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading
import pymongo

from pip_services_commons.config import ConfigParams, IConfigurable
from pip_services_commons.auth import CredentialParams, CredentialResolver
from pip_services_commons.connect import ConnectionParams, ConnectionResolver
from pip_services_commons.refer import IReferenceable
from pip_services_commons.run import IOpenable, ICleanable
from pip_services_commons.log import CompositeLogger
from pip_services_commons.data import PagingParams, DataPage, IdGenerator
from pip_services_commons.errors import ConfigException, ConnectionException

class MongoDbPersistence(object, IReferenceable, IConfigurable, IOpenable, ICleanable):
    _default_config = ConfigParams.from_tuples(
        "collection", None,

        "connection.type", "mongodb",
        "connection.database", "test",
        "connection.host", "localhost",
        "connection.port", 27017,

        "options.max_pool_size", 2,
        "options.keep_alive", True,
        "options.connect_timeout", 30000,
        "options.socket_timeout", 5000,
        "options.auto_reconnect", True,
        "options.max_page_size", 100,
        "options.debug", True
    )

    _lock = None
    _logger = None
    _credential_resolver = None
    _connection_resolver = None
    _options = None

    _database_name = None
    _collection_name = None
    _database = None
    _collection = None
    _client = None

    def __init__(self, collection = None):
        self._lock = threading.Lock()
        self._logger = CompositeLogger()
        self._credential_resolver = CredentialResolver()
        self._connection_resolver = ConnectionResolver()
        self._options = ConfigParams()

        self._collection_name = collection


    def set_references(self, references):
        self._logger.set_references(references)
        self._connection_resolver.set_references(references)
        self._credential_resolver.set_references(references)


    def configure(self, config):
        config = config.set_defaults(self._default_config)
        self._logger.configure(config)
        self._connection_resolver.configure(config)
        self._credential_resolver.configure(config)

        self._collection_name = config.get_as_string_with_default('collection', self._collection_name)
        self._options = self._options.override(config.get_section('options'))


    def _convert_to_public(self, value):
        if value == None: return None
        value['id'] = value['_id']
        value.pop('_id', None)
        return value


    def _convert_from_public(self, value):
        return value


    def is_opened(self):
        return self._client != None and self._database != None

    def open(self, correlation_id):
        credential = self._credential_resolver.lookup(correlation_id)

        connections = self._connection_resolver.resolve_all(correlation_id)
        if connections == None or len(connections) == 0:
            raise ConfigException(correlation_id, "NO_CONNECTION", "Database connection is not set")

        hosts = ''
        uri = None
        self._database_name = ''

        for connection in connections:
            uri = connection.get_uri()
            if uri != None: break

            host = connection.get_host()
            if host == None:
                raise ConfigException(correlation_id, "NO_HOST", "Connection host is not set")

            port = connection.get_port()
            if port == 0:
                raise ConfigException(correlation_id, "NO_PORT", "Connection port is not set")

            if len(hosts) > 0:
                hosts = hosts + ','
            hosts = hosts + host + (':' + str(port) if port != None else '')

            self._database_name = connection.get_as_nullable_string("database")
            if self._database_name == None:
                raise ConfigException(correlation_id, "NO_DATABASE", "Connection database is not set")

        if uri == None:
            uri = "mongodb://" + hosts + "/" + self._database_name

        username = credential.get_username() if credential != None else None
        password = credential.get_password() if credential != None else None

        max_pool_size = self._options.get_as_nullable_integer("max_pool_size")
        keep_alive = self._options.get_as_nullable_boolean("keep_alive")
        connect_timeout = self._options.get_as_nullable_integer("connect_timeout")
        socket_timeout = self._options.get_as_nullable_integer("socket_timeout")
        auto_reconnect = self._options.get_as_nullable_boolean("auto_reconnect")
        max_page_size = self._options.get_as_nullable_integer("max_page_size")
        debug = self._options.get_as_nullable_boolean("debug")

        self._logger.debug(correlation_id, "Connecting to mongodb database " + self._database_name)

        try:
            kwargs = { 
                'maxPoolSize': max_pool_size, 
                'connectTimeoutMS': connect_timeout, 
                'socketKeepAlive': keep_alive,
                'socketTimeoutMS': socket_timeout,
                'appname': correlation_id
            }
            self._client = pymongo.MongoClient(uri, **kwargs)

            self._database = self._client[self._database_name]
            if username != None:
                    self._database.authenticate(username, password)

            self._collection = self._database[self._collection_name]

        except Exception as ex:
            raise ConnectionException(correlation_id, "CONNECT_FAILED", "Connection to mongodb failed") \
                .with_cause(ex)


    def close(self, correlation_id):
        try:
            if self._client != None:
                self._client.close()

            self._collection = None
            self._database = None
            self._client = None

            self._logger.debug(correlation_id, "Disconnected from mongodb database " + str(self._database_name))
        except Exception as ex:
            raise ConnectionException(None, 'DISCONNECT_FAILED', 'Disconnect from mongodb failed: ' + str(ex)) \
                .with_cause(ex)


    def clear(self, correlation_id):
        if self._collection_name == None:
            raise Exception("Collection name is not defined")

        self._database.drop_collection(self._collection_name)