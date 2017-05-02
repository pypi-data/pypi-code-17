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
"""Pluggable Authentication Service Tests
"""
__docformat__ = "reStructuredText"

import doctest
import unittest
import re

from zope import component
from zope.annotation.attribute import AttributeAnnotations
from zope.authentication.interfaces import IAuthentication
from zope.browsermenu.menu import getFirstMenuItem

from zope.component import getUtility
from zope.component import provideUtility, provideAdapter, provideHandler
from zope.component.eventtesting import PlacelessSetup as EventPlacelessSetup
from zope.component.eventtesting import getEvents, clearEvents
from zope.component.hooks import setSite
from zope.component.hooks import setHooks
from zope.component.hooks import resetHooks
from zope.component.interfaces import IComponentLookup
from zope.component.interfaces import ISite
from zope.component.testing import tearDown

from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable

from zope.interface import Interface
from zope.interface import implementer

from zope.password.testing import setUpPasswordManagers
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin

from zope.publisher import base
from zope.publisher.browser import BrowserPage
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IRequest
from zope.publisher.interfaces.browser import IBrowserPublisher

from zope.session.http import CookieClientIdManager
from zope.session.interfaces import IClientId, IClientIdManager, ISession, ISessionDataContainer
from zope.session.session import ClientId, Session, PersistentSessionDataContainer

from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager
from zope.site.site import SiteManagerAdapter

from zope.testing import renormalizing
from zope.testing.cleanup import CleanUp

from zope.traversing import api as traversing
from zope.traversing.interfaces import ITraversable


def setUpTraversal():
    from zope.traversing.testing import setUp as tSetUp
    tSetUp()
    component.provideAdapter(ContainerTraversable,
                             (ISimpleReadContainer,),
                             ITraversable)

def setUpAnnotations():
    component.provideAdapter(AttributeAnnotations)

def setUpSiteManagerLookup():
    component.provideAdapter(SiteManagerAdapter,
                             (Interface,),
                             IComponentLookup)

def createSiteManager(folder, setsite=False):
    if not ISite.providedBy(folder):
        folder.setSiteManager(LocalSiteManager(folder))
    if setsite:
        setSite(folder)
    return traversing.traverse(folder, "++etc++site")


class PlacelessSetup(EventPlacelessSetup,
                     CleanUp):

    def setUp(self, doctesttest=None):
        EventPlacelessSetup.setUp(self)

        setUpPasswordManagers()


setUp = PlacelessSetup().setUp

def placefulSetUp(site=False):
    PlacelessSetup().setUp()
    setHooks()
    setUpTraversal()

    if site:
        site = rootFolder()
        createSiteManager(site, setsite=True)
        return site

def placefulTearDown():
    PlacelessSetup().tearDown()
    resetHooks()
    setSite()

def siteSetUp(test):
    placefulSetUp(site=True)

def siteTearDown(test):
    placefulTearDown()

def nonHTTPSessionTestCaseSetUp(sdc_class=PersistentSessionDataContainer):
    # I am getting an error with ClientId and not TestClientId
    setUp()
    provideAdapter(ClientId, [IRequest], IClientId)
    provideAdapter(Session, [IRequest], ISession)
    provideUtility(CookieClientIdManager(), IClientIdManager)
    sdc = sdc_class()
    provideUtility(sdc, ISessionDataContainer, '')


class NonHTTPSessionTestCase(unittest.TestCase):
    # Small test suite to catch an error with non HTTP protocols, like FTP
    # and SessionCredentialsPlugin.
    def setUp(self):
        nonHTTPSessionTestCaseSetUp()

    def tearDown(self):
        placefulTearDown()

    def test_exeractCredentials(self):
        plugin = SessionCredentialsPlugin()

        self.assertEqual(plugin.extractCredentials(base.TestRequest('/')), None)

    def test_challenge(self):
        plugin = SessionCredentialsPlugin()

        self.assertEqual(plugin.challenge(base.TestRequest('/')), False)

    def test_logout(self):
        plugin = SessionCredentialsPlugin()

        self.assertEqual(plugin.logout(base.TestRequest('/')), False)

class TestPlacesssetup(unittest.TestCase):

    def test_runs(self):
        from zope.app.authentication import placelesssetup
        placelesssetup.PlacelessSetup().setUp()



@implementer(IBrowserPublisher)
class ManagementViewSelector(BrowserView):
    """View that selects the first available management view.

    Support 'zmi_views' actions like: 'javascript:alert("hello")',
    '../view_on_parent.html' or '++rollover++'.
    """
    # Copied from zope.app.publication
    # Simplified to assert just the test case we expect.

    def browserDefault(self, request):
        return self, ()

    def __call__(self):
        item = getFirstMenuItem('zmi_views', self.context, self.request)
        assert item
        redirect_url = item['action']
        if not redirect_url.lower().startswith(('../', 'javascript:', '++')):
            self.request.response.redirect(redirect_url)
            return u''
        raise AssertionError("Should not get here") # pragma: no cover


class Unauthorized(BrowserPage):

    def template(self):
        return "You are not authorized"

    def __call__(self):
        # Set the error status to 403 (Forbidden) in the case when we don't
        # challenge the user
        self.request.response.setStatus(403)

        # make sure that squid does not keep the response in the cache
        self.request.response.setHeader('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT')
        self.request.response.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.request.response.setHeader('Pragma', 'no-cache')

        principal = self.request.principal
        auth = getUtility(IAuthentication)
        auth.unauthorized(principal.id, self.request)
        if self.request.response.getStatus() not in (302, 303):
            return self.template()

checker = renormalizing.RENormalizing([
    (re.compile("u('[^']*?')"), r"\1"),
    (re.compile('u("[^"]*?")'), r"\1"),
])


def test_suite():
    flags = (doctest.NORMALIZE_WHITESPACE
             | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2
             | doctest.ELLIPSIS)
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.app.authentication.interfaces'),
        doctest.DocTestSuite('zope.app.authentication.password'),
        doctest.DocTestSuite('zope.app.authentication.generic'),
        doctest.DocTestSuite('zope.app.authentication.httpplugins'),
        doctest.DocTestSuite('zope.app.authentication.ftpplugins'),
        doctest.DocTestSuite('zope.app.authentication.groupfolder'),
        doctest.DocFileSuite('principalfolder.rst',
                             optionflags=flags,
                             checker=checker,
                             setUp=setUp,
                             tearDown=tearDown),
        doctest.DocTestSuite('zope.app.authentication.principalfolder',
                             optionflags=flags,
                             checker=checker,
                             setUp=setUp,
                             tearDown=tearDown),
        doctest.DocTestSuite('zope.app.authentication.idpicker'),
        doctest.DocTestSuite('zope.app.authentication.session',
                             optionflags=flags,
                             checker=checker,
                             setUp=siteSetUp,
                             tearDown=siteTearDown),
        doctest.DocFileSuite('README.rst',
                             setUp=siteSetUp,
                             tearDown=siteTearDown,
                             optionflags=flags,
                             checker=checker,
                             globs={'provideUtility': provideUtility,
                                    'provideAdapter': provideAdapter,
                                    'provideHandler': provideHandler,
                                    'getEvents': getEvents,
                                    'clearEvents': clearEvents,
                                    }),
        doctest.DocFileSuite('groupfolder.rst',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=flags,
                             checker=checker,
                             ),
        doctest.DocFileSuite('vocabulary.rst',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=flags,
                             checker=checker,
                             ),
        unittest.defaultTestLoader.loadTestsFromName(__name__)
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
