import importlib

from six import string_types

from feedz import conf

BACKEND_ALIASES = {
    "database": "feedz.backends.database.DatabaseBackend",
    #"redis": "feedz.backends.pyredis.RedisBackend",
}

_backend_cache = {}


def symbol_by_name(name, aliases=None, imp=None, package=None,
        sep='.', default=None, **kwargs):
    """Get symbol by qualified name.

    The name should be the full dot-separated path to the class::

        modulename.ClassName

    Example::

        celery.concurrency.processes.TaskPool
                                    ^- class name

    or using ':' to separate module and symbol::

        celery.concurrency.processes:TaskPool

    If `aliases` is provided, a dict containing short name/long name
    mappings, the name is looked up in the aliases first.

    Examples:

        >>> symbol_by_name("celery.concurrency.processes.TaskPool")
        <class 'celery.concurrency.processes.TaskPool'>

        >>> symbol_by_name("default", {
        ...     "default": "celery.concurrency.processes.TaskPool"})
        <class 'celery.concurrency.processes.TaskPool'>

        # Does not try to look up non-string names.
        >>> from celery.concurrency.processes import TaskPool
        >>> symbol_by_name(TaskPool) is TaskPool
        True
    """
    aliases = aliases or {}

    if imp is None:
        imp = importlib.import_module

    if not isinstance(name, string_types):
        # already a class
        return name

    name = aliases.get(name) or name
    sep = ':' if ':' in name else sep
    module_name, _, cls_name = name.rpartition(sep)
    if not module_name:
        cls_name, module_name = None, package if package else cls_name
    try:
        try:
            module = imp(module_name, package=package, **kwargs)
        except ValueError as e:
            raise ValueError("Couldn't import %r: %s" % (name, e))
        return getattr(module, cls_name) if cls_name else module
    except (ImportError, AttributeError):
        if default is None:
            raise
    return default


def get_backend_cls(backend):
    if backend not in _backend_cache:
        _backend_cache[backend] = symbol_by_name(backend, BACKEND_ALIASES)
    return _backend_cache[backend]


def backend_or_default(backend=None):
    backend = backend or conf.POST_STORAGE_BACKEND
    if isinstance(backend, string_types):
        return get_backend_cls(backend)()
    return backend
