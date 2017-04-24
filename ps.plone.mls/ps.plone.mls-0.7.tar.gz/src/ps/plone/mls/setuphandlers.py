# -*- coding: utf-8 -*-
"""Post install import steps for ps.plone.mls."""

# zope imports
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'ps.plone.mls:testfixture',
            'ps.plone.mls:uninstall',
        ]
