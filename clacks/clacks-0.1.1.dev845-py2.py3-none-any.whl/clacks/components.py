#!/usr/bin/env python3

""" PHP migrated components collection. Hopefully will be replaced
    by controls someday... """

import importlib

from . import component as _cpkg
from .core import cfg


def fetchByType(page_type):
    """ return components list created from config file for page_type given """

    config = cfg.get('components', 'page_types', page_type, default=None)
    if config is None:
        config = cfg.get('components', 'page_types', 'default')
    components = []

    for component in config:
        mod = importlib.import_module('.'+component['class'], _cpkg.__package__)  # pylint: disable=no-member
        if isinstance(component['params'], dict):
            components.append(getattr(mod, component['class'])(**component['params']))
        else:
            components.append(getattr(mod, component['class'])(*component['params']))
    return components
