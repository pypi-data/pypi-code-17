"""Plugin manager module."""

from __future__ import absolute_import, division, print_function

from byte import __path__ as byte_path
from byte.compilers.core.base import CompilerPlugin
from byte.core.plugin.base import Plugin
from byte.executors.core.base import ExecutorPlugin
from byte.formats.core.base import CollectionFormatPlugin, DocumentFormatPlugin

import imp
import inspect
import logging
import os
import pkgutil
import sys

log = logging.getLogger(__name__)


class PluginManager(object):
    """Plugin manager class."""

    kinds = [
        'compiler',
        'executor',
        'format'
    ]

    collections = {
        CompilerPlugin: [
            ('compilers_by_content_type',           'content_type'),    # noqa
            ('compilers_by_extension',              'extension')        # noqa
        ],
        ExecutorPlugin: [
            ('executors_by_content_type',           'content_type'),    # noqa
            ('executors_by_extension',              'extension'),       # noqa
            ('executors_by_scheme',                 'scheme')           # noqa
        ],
        CollectionFormatPlugin: [
            ('collection_formats_by_content_type',  'content_type'),    # noqa
            ('collection_formats_by_extension',     'extension')        # noqa
        ],
        DocumentFormatPlugin: [
            ('document_formats_by_content_type',    'content_type'),    # noqa
            ('document_formats_by_extension',       'extension')        # noqa
        ]
    }

    def __init__(self, modules=None):
        """Create plugin manager.

        :param modules: Default plugin modules
        :type modules: list of module or None
        """
        # Compilers
        self.compilers_by_content_type = {}
        self.compilers_by_extension = {}

        # Executors
        self.executors_by_content_type = {}
        self.executors_by_extension = {}
        self.executors_by_scheme = {}

        # Formats
        self.collection_formats_by_content_type = {}
        self.collection_formats_by_extension = {}

        self.document_formats_by_content_type = {}
        self.document_formats_by_extension = {}

        # Plugins
        self.plugins = {}
        self.plugins_by_kind = {}

        # Update plugin registry
        self.update(modules, reset=False)

    @classmethod
    def discover(cls, packages=('compilers', 'executors', 'formats')):
        """Discover plugin modules.

        :param packages: Package names
        :type packages: tuple of str
        """
        scanned_paths = set()

        for search_path in byte_path:
            search_path = os.path.normcase(os.path.normpath(
                os.path.realpath(search_path)
            ))

            if search_path in scanned_paths:
                continue

            scanned_paths.add(search_path)

            # Scan `search_path` for `packages`
            for package in packages:
                # Find package
                try:
                    _, package_path, _ = imp.find_module(package, [search_path])
                except ImportError:
                    continue

                # Discover plugins in package
                for mod in cls.discover_package(package, package_path):
                    yield mod

    @staticmethod
    def discover_package(package, package_path):
        """Discover plugin modules in package.

        :param package: Package name
        :type package: str

        :param package_path: Package path
        :type package_path: str
        """
        # Iterate over modules in package
        for _, name, _ in pkgutil.iter_modules([package_path]):
            # Find module
            try:
                fp, module_path, description = imp.find_module(name, [package_path])
            except ImportError as ex:
                log.warn('Unable to find module \'%s\' in %r: %s', name, package_path, ex)
                continue

            # Return existing module (if available)
            full_name = 'byte.%s.%s' % (package, name)

            if full_name in sys.modules:
                yield sys.modules[full_name]
                continue

            # Import module
            try:
                yield imp.load_module(full_name, fp, module_path, description)
            except ImportError as ex:
                log.warn('Unable to load module \'%s\' in %r: %s', name, module_path, ex)
                continue

    def get(self, kind, key):
        """Get plugin.

        Raises :code:`ValueError` on unknown plugin type or key.

        :param kind: Plugin type
        :type kind: str

        :param key: Plugin key
        :type key: str
        """
        if kind not in self.kinds:
            raise ValueError('Unknown plugin kind: %s' % (kind,))

        # Retrieve plugins matching `kind`
        plugins = self.plugins_by_kind.get(kind)

        if not plugins:
            raise ValueError('No \'%s\' plugins have been registered' % (kind,))

        # Return plugin matching `key` (if one exists)
        plugin = plugins.get(key)

        if not plugin:
            raise ValueError('No \'%s\' %s available' % (key, kind))

        return plugin

    def get_compiler(self, key):
        """Retrieve compiler by key.

        :param key: Key
        :type key: str
        """
        return self.plugins_by_kind.get('compiler', {})[key]

    def get_compiler_by_content_type(self, content_type):
        """Retrieve compiler by content type.

        :param content_type: Content type
        :type content_type: str
        """
        compilers = self.compilers_by_content_type.get(content_type)

        if not compilers:
            raise KeyError(content_type)

        _, compiler = compilers[0]
        return compiler

    def get_compiler_by_extension(self, extension):
        """Retrieve compiler by file extension.

        :param extension: File extension
        :type extension: str
        """
        compilers = self.compilers_by_extension.get(extension)

        if not compilers:
            raise KeyError(extension)

        _, compiler = compilers[0]
        return compiler

    def get_executor_by_scheme(self, scheme):
        """Retrieve executor by URI scheme.

        :param scheme: URI Scheme
        :type scheme: str
        """
        executors = self.executors_by_scheme.get(scheme)

        if not executors:
            raise KeyError(scheme)

        _, executor = executors[0]
        return executor

    def get_collection_format_by_content_type(self, content_type):
        """Retrieve collection format by content type.

        :param content_type: Content type
        :type content_type: str
        """
        compilers = self.collection_formats_by_content_type.get(content_type)

        if not compilers:
            raise KeyError(content_type)

        _, compiler = compilers[0]
        return compiler

    def get_collection_format_by_extension(self, extension):
        """Retrieve collection format by file extension.

        :param extension: File extension
        :type extension: str
        """
        compilers = self.collection_formats_by_extension.get(extension)

        if not compilers:
            raise KeyError(extension)

        _, compiler = compilers[0]
        return compiler

    def get_document_format_by_content_type(self, content_type):
        """Retrieve document format by content type.

        :param content_type: Content type
        :type content_type: str
        """
        compilers = self.document_formats_by_content_type.get(content_type)

        if not compilers:
            raise KeyError(content_type)

        _, compiler = compilers[0]
        return compiler

    def get_document_format_by_extension(self, extension):
        """Retrieve document format by file extension.

        :param extension: File extension
        :type extension: str
        """
        compilers = self.document_formats_by_extension.get(extension)

        if not compilers:
            raise KeyError(extension)

        _, compiler = compilers[0]
        return compiler

    def register(self, plugin):
        """Register plugin.

        :param plugin: Plugin
        """
        # Ensure plugin has a "key" defined
        if plugin.key is None:
            log.warn('Plugin \'%s\' in module \'%s\' has no "key" property defined', plugin.__name__, plugin.__module__)
            return False

        # Resolve plugin meta
        meta = getattr(plugin, 'Meta', None)

        if not meta:
            log.warn('Plugin \'%s\' has no meta defined', plugin.key)
            return False

        # Transform plugin meta values
        meta.transform()

        # Validate plugin meta
        try:
            meta.validate(plugin)
        except AssertionError as ex:
            log.warn('Plugin \'%s\' failed validation: %s', plugin.key, ex.message)
            return False

        # Ensure plugin `meta.kind` collection exists
        if meta.kind not in self.plugins_by_kind:
            self.plugins_by_kind[meta.kind] = {}

        # Ensure plugin hasn't already been registered
        if (meta.kind, plugin.key) in self.plugins or plugin.key in self.plugins_by_kind[meta.kind]:
            log.warn('Plugin with kind \'%s\' and key \'%s\' has already been registered', meta.kind, plugin.key)
            return False

        # Register plugin
        self.plugins[(meta.kind, plugin.key)] = plugin
        self.plugins_by_kind[meta.kind][plugin.key] = plugin

        # Register plugin in collections
        self.register_collections(plugin, meta)

        log.debug('Registered %s \'%s\'', meta.kind, plugin.key)
        return True

    def register_collections(self, plugin, meta):
        """Register plugin in collections.

        :param plugin: Plugin
        :param meta: Plugin metadata
        """
        for cls, collections in self.collections.items():
            if not issubclass(plugin, cls):
                continue

            for name, attribute in collections:
                # Retrieve collection dictionary
                collection = getattr(self, name)

                if collection is None:
                    raise ValueError('Unknown collection: %s' % (name,))

                # Register plugin in collection
                self.register_attribute(collection, attribute, plugin, meta)

    def register_attribute(self, collection, attribute, plugin, meta):
        """Register plugin in collection.

        :param collection: Plugin collection
        :type collection: dict

        :param attribute: Attribute name
        :type attribute: str

        :param plugin: Plugin
        :param meta: Plugin metadata
        """
        for value in (getattr(meta, attribute) or []):
            priority, value = self._resolve_definition(value)

            # Ensure `attribute` collection exists
            if value not in collection:
                collection[value] = []

            # Register plugin by `attribute`
            collection[value].append((plugin.priority + (priority / 10), plugin))
            collection[value].sort()

    def reset(self):
        """Reset plugin registry."""
        self.executors_by_scheme = {}

        self.plugins = {}
        self.plugins_by_kind = {}

    def update(self, modules=None, reset=True):
        """Update plugins registry.

        :param modules: Modules to scan for plugins
        :type modules: list of module

        :param reset: Reset registry
        :type reset: bool
        """
        # Reset state (if enabled)
        if reset:
            self.reset()

        # Find (and register) plugin classes in `modules`
        for mod in (modules or self.discover()):
            for key, value in mod.__dict__.items():
                if key.startswith('_') or not inspect.isclass(value):
                    continue

                if value.__module__ != mod.__name__ and value.__module__ != mod.__name__ + '.main':
                    continue

                if not issubclass(value, Plugin):
                    continue

                self.register(value)

    @staticmethod
    def _resolve_definition(value):
        if type(value) is tuple and len(value) == 2:
            return value

        return 1000, value

    def __contains__(self, key):
        return key in self.plugins

    def __len__(self):
        return len(self.plugins)
