#!/usr/bin/env python3

"""Imports all classes from gtcms.model package modules

This import is done here so that it doesn't create strange
class name - module name conflict as when it was done in
model.__init__ case.
"""


def __getModelClasses():
    """Import all classes not leaking any additional declarations"""

    import pkgutil
    from importlib import import_module
    from . import model
    package = '.'.join(model.__name__.split('.')[:-1])
    for mdata in pkgutil.iter_modules(model.__path__):
        mod = import_module('.'.join([package, 'model', mdata[1]]))
        globals()[mdata[1]] = getattr(mod, mdata[1])

    del globals()['__getModelClasses']

if __name__ != '__main__':
    __getModelClasses()
