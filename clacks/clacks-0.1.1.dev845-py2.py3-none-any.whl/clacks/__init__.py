#!/usr/bin/env python3

"""Imports shims"""

import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)


def __configure():
    """Import "shims" - useful patches to other libraries that make life easier
       Warning: shims should not import anything from this package or do so
                in a way preventing dependency loops
    """
    import importlib
    try:
        from . import _shim
    except ImportError:
        pass
    else:
        for mdata in pkgutil.iter_modules(_shim.__path__):
            mod = importlib.import_module('.'+mdata[1], _shim.__name__)
            if hasattr(mod, 'configure'):
                mod.configure()

__configure()
del __configure
