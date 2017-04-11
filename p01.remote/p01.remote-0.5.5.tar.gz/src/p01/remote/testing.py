##############################################################################
#
# Copyright (c) 2008 Projekt01 GmbH and Contributors.
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
"""
$Id:$
"""
__docformat__ = "reStructuredText"

import logging
import time

import zope.interface
import zope.component
from zope.schema import ValidationError

from p01.remote import job
from p01.remote import exceptions
from p01.remote import processor


###############################################################################
#
# Testing stubs
#
###############################################################################

class EchoJob(job.Job):
    """A simple echo, job implementation."""

    def __call__(self, remoteProcessor):
        return self.input


class SleepJob(job.Job):
    """Sleep job."""

    def __call__(self, remoteProcessor):
        (sleepTime, id) = self.input
        time.sleep(sleepTime)
        log = logging.getLogger('p01.remote')
        log.info('Job: %i' %id)


class ErrorJob(job.Job):
    """A simple error job for testing."""

    def __call__(self, remoteProcessor):
        raise exceptions.JobError('An error occurred.')


class FatalJob(job.Job):
    """A fatal error for testing"""

    def __call__(self, remoteProcessor):
        raise ValidationError('An error occurred.')



###############################################################################
#
# remove zope.app.testing dependency
# zope.app.testing.placelesssetup

from zope.schema.vocabulary import setVocabularyRegistry
from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.component.eventtesting import PlacelessSetup as EventPlacelessSetup
from zope.i18n.testing import PlacelessSetup as I18nPlacelessSetup
from zope.password.testing import setUpPasswordManagers
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.browser.absoluteurl import AbsoluteURL

from zope.container.testing import PlacelessSetup as ContainerPlacelessSetup
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


stypes = list, tuple
def provideAdapter(required, provided, factory, name='', with_=(), **kw):
    if with_ is None and kw.has_key('with'):
        with_ = kw['with']
    if isinstance(factory, (list, tuple)):
        raise ValueError("Factory cannot be a list or tuple")
    gsm = zope.component.getGlobalSiteManager()

    if with_:
        required = (required, ) + tuple(with_)
    elif not isinstance(required, stypes):
        required = (required,)

    gsm.registerAdapter(factory, required, provided, name, event=False)

def browserView(for_, name, factory, layer=IDefaultBrowserLayer,
                providing=zope.interface.Interface):
    """Define a global browser view
    """
    if isinstance(factory, (list, tuple)):
        raise ValueError("Factory cannot be a list or tuple")
    provideAdapter(for_, providing, factory, name, (layer,))

def browserViewProviding(for_, factory, providing, layer=IDefaultBrowserLayer):
    """Define a view providing a particular interface."""
    if isinstance(factory, (list, tuple)):
        raise ValueError("Factory cannot be a list or tuple")
    return browserView(for_, '', factory, layer, providing)


class PlacelessSetup(CAPlacelessSetup,
                     EventPlacelessSetup,
                     I18nPlacelessSetup,
                     ContainerPlacelessSetup):

    def setUp(self, doctesttest=None):
        CAPlacelessSetup.setUp(self)
        EventPlacelessSetup.setUp(self)
        ContainerPlacelessSetup.setUp(self)
        I18nPlacelessSetup.setUp(self)

        setUpPasswordManagers()
        browserView(None, 'absolute_url', AbsoluteURL)
        browserViewProviding(None, AbsoluteURL, IAbsoluteURL)

        from zope.security.testing import addCheckerPublic
        addCheckerPublic()

        from zope.security.management import newInteraction
        newInteraction()

        setVocabularyRegistry(None)


ps = PlacelessSetup()
placelessSetUp = ps.setUp

def tearDown():
    tearDown_ = ps.tearDown
    def tearDown(doctesttest=None):
        tearDown_()
    return tearDown

placelessTearDown = tearDown()

del ps

###############################################################################
#
# remove zope.app.testing dependency
# zope.app.testing.setup

#------------------------------------------------------------------------
# Annotations
from zope.annotation.attribute import AttributeAnnotations
def setUpAnnotations():
    zope.component.provideAdapter(AttributeAnnotations)

#------------------------------------------------------------------------
# Traversal
from zope.traversing.interfaces import ITraversable
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
def setUpTraversal():
    from zope.traversing.testing import setUp
    setUp()
    zope.component.provideAdapter(ContainerTraversable,
                                  (ISimpleReadContainer,), ITraversable)

#------------------------------------------------------------------------
# ISiteManager lookup
from zope.site.site import SiteManagerAdapter
from zope.component.interfaces import IComponentLookup
from zope.interface import Interface
def setUpSiteManagerLookup():
    zope.component.provideAdapter(SiteManagerAdapter, (Interface,),
                                  IComponentLookup)



#------------------------------------------------------------------------
# Sample Folder Creation
import zope.traversing.api
from zope.site.site import LocalSiteManager
import zope.component.interfaces

def createSiteManager(folder, setsite=False):
    if not zope.component.interfaces.ISite.providedBy(folder):
        folder.setSiteManager(LocalSiteManager(folder))
    if setsite:
        zope.component.hooks.setSite(folder)
    return zope.traversing.api.traverse(folder, "++etc++site")

#------------------------------------------------------------------------
from zope.site.folder import rootFolder

def placefulSetUp(site=False):
    placelessSetUp()
    zope.component.hooks.setHooks()
    setUpAnnotations()
    setUpTraversal()
    setUpSiteManagerLookup()
    if site:
        site = rootFolder()
        createSiteManager(site, setsite=True)
        return site

def placefulTearDown():
    placelessTearDown()
    zope.component.hooks.resetHooks()
    zope.component.hooks.setSite()


###############################################################################
#
# testing setup
#
###############################################################################
from zope.testing.loggingsupport import InstalledHandler


def setUp(test):
    root = placefulSetUp(site=True)
    test.globs['root'] = root

    log_info = InstalledHandler('p01.remote')
    test.globs['log_info'] = log_info
    test.origArgs = processor.RemoteProcessor.workerArguments
    processor.RemoteProcessor.workerArguments = {'waitTime': 0.0}


def tearDown(test):
    placefulTearDown()
    log_info = test.globs['log_info']
    log_info.clear()
    log_info.uninstall()
    processor.RemoteProcessor.workerArguments = test.origArgs
