#!/usr/bin/env python3

"""Simple Chameleon templates wrapper."""

# pylint: disable=unused-argument

import os
import types

from ..core import ROOTPATH
from ..gettext import gettext as _

os.environ['CHAMELEON_CACHE'] = str(ROOTPATH/'caches/chameleon')

from chameleon import PageTemplateLoader  # pylint: disable=wrong-import-order,wrong-import-position


def _translate(msgid, domain=None, mapping=None, default=None, context=None):
    """Template translations support function"""

    if domain == 'python':
        return _(msgid)
    return msgid


templates = PageTemplateLoader([str(ROOTPATH/'template')],
                               '.pt',
                               translate=_translate,
                               trim_attribute_space=True)


def first(self, *names):
    """Return first template found"""
    try:
        return self[next(f for f in names if (ROOTPATH/'template'/(f+'.pt')).is_file())]
    except StopIteration:
        raise KeyError("No matching template found: %r" % (names,))

templates.first = types.MethodType(first, templates)
del first
