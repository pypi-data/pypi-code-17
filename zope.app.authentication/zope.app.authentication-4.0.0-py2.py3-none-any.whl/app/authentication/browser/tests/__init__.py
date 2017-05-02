##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"Test helpers; not public API"

from zope import component

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


def provideUtility(provided, utility, name=''):
    gsm = component.getGlobalSiteManager()
    gsm.registerUtility(utility, provided, name, event=False)

stypes = list, tuple
def provideAdapter(required, provided, factory, name='', using=None, **kw):
    assert 'with' not in kw
    assert not isinstance(factory, stypes), "Factory cannot be a list or tuple"

    gsm = component.getGlobalSiteManager()

    if using:
        required = (required, ) + tuple(using)
    elif not isinstance(required, stypes):
        required = (required,)

    gsm.registerAdapter(factory, required, provided, name, event=False)

def browserView(for_, name, factory, layer=IDefaultBrowserLayer,
                providing=Interface):
    """Define a global browser view
    """
    provideAdapter(for_, providing, factory, name, (layer,))

def browserViewProviding(for_, factory, providing, layer=IDefaultBrowserLayer):
    """Define a view providing a particular interface."""
    return browserView(for_, '', factory, layer, providing)

def provideMultiView(for_, type, providing, name, factory, layer=None):
    if layer is None:
        layer = type
    provideAdapter(for_[0], providing, factory, name, tuple(for_[1:])+(layer,))
