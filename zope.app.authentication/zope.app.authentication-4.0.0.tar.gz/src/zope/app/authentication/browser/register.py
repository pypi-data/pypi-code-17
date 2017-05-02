##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Improved registration UI for registering pluggable authentication utilities
"""

from zope.app.authentication.i18n import ZopeMessageFactory as _
from zope.app.component.browser.registration import AddUtilityRegistration
from zope.authentication.interfaces import IAuthentication

class AddAuthenticationRegistration(AddUtilityRegistration):

    label = _("Register a pluggable authentication utility")
    name = ''
    provided = IAuthentication
