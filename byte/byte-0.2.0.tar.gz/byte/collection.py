# -*- coding: utf-8 -*-

"""Contains the collection structure for the storage of keyed items."""

from __future__ import absolute_import, division, print_function

from byte.core.plugin.manager import PluginManager
from byte.executors.core.base import Executor
from byte.model import Model
from byte.statements import DeleteStatement, InsertStatement, SelectStatement, UpdateStatement

from six import string_types
from six.moves.urllib.parse import parse_qsl, urlparse
import inspect
import logging

log = logging.getLogger(__name__)


class CollectionError(Exception):
    """Generic collection error."""


class CollectionLoadError(CollectionError):
    """Collection couldn't be loaded."""


class CollectionModelError(CollectionError):
    """Collection model violation."""


class CollectionParseError(CollectionError):
    """Collection parse error."""


class CollectionValidationError(CollectionError):
    """Collection item violation error."""


class Collection(object):
    """Collection for the storage of keyed items."""

    def __init__(self, model_or_uri=None, uri=None, model=None, executor=None, plugins=None):
        """
        Create keyed item collection.

        :param uri: Data Source URI
        :type uri: str

        :param model: Collection data model
        :type model: class

        :param executor: Collection executor
        :type executor: byte.executors.core.base.Executor or type

        :param plugins: List of plugins to enable for the collection (if :code:`None` is provided
                        all plugins will be enabled)
        :type plugins: list
        """
        self.model = None

        self.uri = None
        self.parameters = {}

        self._executor = None
        self._executor_cls = None

        self.plugins = None

        # Parse dynamic parameter
        if model_or_uri:
            if inspect.isclass(model_or_uri) and issubclass(model_or_uri, Model):
                model = model_or_uri
            elif isinstance(model_or_uri, string_types):
                uri = model_or_uri
            else:
                raise ValueError('Unknown initialization parameter value (expected subclass of Model, or string)')

        # Parse keyword parameters
        if model:
            self.model = model

        # Construct plugin manager
        self.plugins = PluginManager(plugins)

        # Parse URI
        if uri:
            self.uri = urlparse(uri)

            if self.uri.query:
                self.parameters = dict(parse_qsl(self.uri.query))

        # Retrieve executor
        if executor:
            self.executor = executor
        elif uri:
            self.executor = self.plugins.get_executor_by_scheme(self.uri.scheme)

    @property
    def executor(self):
        """Retrieve collection executor.

        :return: Executor
        :rtype: byte.executors.core.base.Executor
        """
        if not self._executor:
            # Ensure executor class is available
            if not self._executor_cls:
                raise CollectionLoadError('No executor available')

            # Construct executor instance
            self._executor = self._executor_cls(
                self,
                self.model
            )

        # Return current executor instance
        return self._executor

    @executor.setter
    def executor(self, value):
        """Set the current collection executor.

        :param value: Executor (class or instance)
        :type value: byte.executors.core.base.Executor or class
        """
        if not value:
            self._executor = None
            self._executor_cls = None
            return

        # Class
        if inspect.isclass(value) and issubclass(value, Executor):
            self._executor = None
            self._executor_cls = value
            return

        # Instance
        if isinstance(value, Executor):
            self._executor = value
            self._executor_cls = None

        # Unknown value
        raise ValueError('Unknown value provided (expected `Executor` class or instance)')

    @property
    def internal(self):
        """Retrieve internal model metadata."""
        if not self.model:
            return None

        return self.model.Internal

    @property
    def properties(self):
        """Retrieve model properties."""
        if not self.model:
            return None

        return self.model.Properties

    def bind(self, model):
        """Bind collection to data model.

        :param model: Data model
        :type model: byte.model.Model
        """
        if not model or not issubclass(model, Model):
            raise CollectionModelError('Invalid value provided for the "model" parameter (expected Model subclass)')

        self.model = model

    def connect(self, prop, collection):
        """Connect collection to relation property.

        :param prop: Relation property
        :type prop: byte.property.RelationProperty

        :param collection: Collection
        :type collection: Collection
        """
        if not prop:
            raise ValueError('Invalid property')

        prop.connect(collection)

    def execute(self, statement):
        """Execute statement.

        :param statement: Statement
        :type statement: byte.statements.core.base.Statement
        """
        if not self.executor:
            raise Exception('No executor available')

        return self.executor.execute(statement)

    def all(self):
        """Retrieve all items from collection."""
        return self.select()

    def delete(self):
        """Create delete statement."""
        return DeleteStatement(self, self.model)

    def select(self, *properties):
        """Create select statement."""
        return SelectStatement(
            self, self.model,
            properties=properties
        )

    def update(self, args, **kwargs):
        """Create update statement."""
        data = kwargs

        for value in args:
            data.update(value)

        return UpdateStatement(
            self, self.model,
            data=data
        )

    def create(self, **kwargs):
        """Create item."""
        if not self.model:
            raise Exception('Collection has no model bound')

        return self.model.create(
            _collection=self,
            **kwargs
        )

    def create_or_get(self):
        """Create (or retrieve the existing) item."""
        raise NotImplementedError

    # TODO Better handling of primary key queries (string values are currently parsed as statements)
    def get(self, *query, **kwargs):
        """Retrieve item."""
        statement = self.select().limit(1)

        if query:
            statement = statement.where(*query)

        if kwargs:
            statement = statement.filter(**kwargs)

        return statement.first()

    def get_or_create(self):
        """Retrieve existing (or create) item."""
        raise NotImplementedError

    def insert(self, *args, **kwargs):
        """Create insert statement."""
        item = kwargs

        for value in args:
            item.update(value)

        return InsertStatement(
            self, self.model,
            items=[item]
        )

    def insert_from(self, query, properties):
        """Create insert from statement."""
        return InsertStatement(
            self, self.model,
            query=query,
            properties=properties
        )

    def insert_many(self, items):
        """Create insert many statement."""
        return InsertStatement(
            self, self.model,
            items=items
        )


# noinspection PyAbstractClass
class CollectionMixin(Collection):
    """Base class for collection mixins."""
