# -*- coding: utf-8 -*-
from cStringIO import StringIO
from plone.app.caching.interfaces import IPloneCacheSettings
from plone.app.caching.testing import PLONE_APP_CACHING_FUNCTIONAL_TESTING
from plone.app.caching.tests.test_utils import stable_now
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.textfield.value import RichTextValue
from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.interfaces import IPurger
from plone.caching.interfaces import ICacheSettings
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from Products.CMFCore.FSFile import FSFile
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.globalrequest import setRequest

import datetime
import dateutil.parser
import dateutil.tz
import os
import pkg_resources
import unittest


TEST_FILE = pkg_resources.resource_filename(
    'plone.app.caching.tests', 'test.gif')


def test_image():
    from plone.namedfile.file import NamedBlobImage
    filename = pkg_resources.resource_filename(
        'plone.app.caching.tests', 'test.gif')
    filename = os.path.join(os.path.dirname(__file__), u'test.gif')
    return NamedBlobImage(
        data=open(filename, 'r').read(),
        filename=filename
    )


def _normalize_etag(s):
    s = s.split('|')
    s.pop()  # remove time-based component
    return '|'.join(s)


class TestProfileWithCaching(unittest.TestCase):
    """This test aims to exercise the caching operations expected from the
    `with-caching-proxy` profile.

    Several of the operations are just duplicates of the ones for the
    `without-caching-proxy` profile but we still want to redo them in this
    context to ensure the profile has set the correct settings.
    """

    layer = PLONE_APP_CACHING_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        test_css = FSFile('test.css', os.path.join(
            os.path.dirname(__file__), 'test.css'))
        self.portal.portal_skins.custom._setOb('test.css', test_css)

        setRequest(self.portal.REQUEST)

        applyProfile(self.portal, 'plone.app.caching:with-caching-proxy')

        self.registry = getUtility(IRegistry)

        self.cacheSettings = self.registry.forInterface(ICacheSettings)
        self.cachePurgingSettings = self.registry.forInterface(
            ICachePurgingSettings)
        self.ploneCacheSettings = self.registry.forInterface(
            IPloneCacheSettings)

        self.cacheSettings.enabled = True

        self.purger = getUtility(IPurger)
        self.purger.reset()

    def tearDown(self):
        setRequest(None)

    def test_composite_views(self):
        # This is a clone of the same test for 'without-caching-proxy'
        # Can we just call that test from this context?

        catalog = self.portal['portal_catalog']
        skins_tool = self.portal['portal_skins']

        # Add folder content
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        self.portal.invokeFactory('Folder', 'f1')
        self.portal['f1'].title = 'one'
        self.portal['f1'].description = u"Folder one description"
        self.portal['f1'].reindexObject()

        # Add page content
        self.portal['f1'].invokeFactory('Document', 'd1')
        self.portal['f1']['d1'].title = u"Document one"
        self.portal['f1']['d1'].description = u"Document one description"
        testText = 'Testing... body one'
        self.portal['f1']['d1'].text = RichTextValue(
            testText,
            'text/plain',
            'text/html'
        )
        self.portal['f1']['d1'].reindexObject()

        # Publish the folder and page
        self.portal.portal_workflow.doActionFor(self.portal['f1'], 'publish')
        self.portal.portal_workflow.doActionFor(
            self.portal['f1']['d1'], 'publish')

        # Should we set up the etag components?
        # - set member?  No
        # - reset catalog counter?  Maybe
        # - set server language?
        # - turn on gzip?
        # - set skin?  Maybe
        # - leave status unlocked
        #

        import transaction
        transaction.commit()

        # Request the authenticated folder
        now = stable_now()
        browser = Browser(self.app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD, ),
        )
        browser.open(self.portal['f1'].absolute_url())
        self.assertEqual('plone.content.folderView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        self.assertEqual('"|test_user_1_|%d|en|%s|0|0' % (catalog.getCounter(
        ), skins_tool.default_skin), _normalize_etag(browser.headers['ETag']))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Set the copy/cut cookie and then request the folder view again
        browser.cookies.create('__cp', 'xxx')
        browser.open(self.portal['f1'].absolute_url())
        # The response should be the same as before except for the etag
        self.assertEqual('plone.content.folderView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        self.assertEqual('"|test_user_1_|%d|en|%s|0|1' % (catalog.getCounter(
        ), skins_tool.default_skin), _normalize_etag(browser.headers['ETag']))

        # Request the authenticated page
        now = stable_now()
        browser = Browser(self.app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD, ),
        )
        browser.open(self.portal['f1']['d1'].absolute_url())
        self.assertIn(testText, browser.contents)
        self.assertEqual('plone.content.itemView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        self.assertEqual('"|test_user_1_|%d|en|%s|0' % (catalog.getCounter(
        ), skins_tool.default_skin), _normalize_etag(browser.headers['ETag']))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the authenticated page again -- to test RAM cache.
        browser = Browser(self.app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD, ),
        )
        browser.open(self.portal['f1']['d1'].absolute_url())
        self.assertEqual('plone.content.itemView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # Authenticated should NOT be RAM cached
        self.assertIsNone(browser.headers.get('X-RAMCache'))

        # Request the authenticated page again -- with an INM header to test
        # 304
        etag = browser.headers['ETag']
        browser = Browser(self.app)
        browser.raiseHttpErrors = False  # we really do want to see the 304
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD, ),
        )
        browser.addHeader('If-None-Match', etag)
        browser.open(self.portal['f1']['d1'].absolute_url())
        # This should be a 304 response
        self.assertEqual('304 Not Modified', browser.headers['Status'])
        self.assertEqual('', browser.contents)

        # Request the anonymous folder
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal['f1'].absolute_url())
        self.assertEqual('plone.content.folderView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        self.assertEqual('"||%d|en|%s|0|0' % (catalog.getCounter(
        ), skins_tool.default_skin), _normalize_etag(browser.headers['ETag']))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the anonymous page
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal['f1']['d1'].absolute_url())
        self.assertEqual('plone.content.itemView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        self.assertIn(testText, browser.contents)
        # This should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        self.assertEqual('"||%d|en|%s|0' % (catalog.getCounter(
        ), skins_tool.default_skin), _normalize_etag(browser.headers['ETag']))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the anonymous page again -- to test RAM cache.
        # Anonymous should be RAM cached
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal['f1']['d1'].absolute_url())
        self.assertEqual('plone.content.itemView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # This should come from RAM cache
        self.assertEqual('plone.app.caching.operations.ramcache',
                         browser.headers['X-RAMCache'])
        self.assertIn(testText, browser.contents)
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        self.assertEqual('"||%d|en|%s|0' % (catalog.getCounter(
        ), skins_tool.default_skin), _normalize_etag(browser.headers['ETag']))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the anonymous page again -- with an INM header to test 304.
        etag = browser.headers['ETag']
        browser = Browser(self.app)
        browser.raiseHttpErrors = False
        browser.addHeader('If-None-Match', etag)
        browser.open(self.portal['f1']['d1'].absolute_url())
        self.assertEqual('plone.content.itemView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # This should be a 304 response
        self.assertEqual('304 Not Modified', browser.headers['Status'])
        self.assertEqual('', browser.contents)

        # Edit the page to update the etag
        testText2 = 'Testing... body two'
        self.portal['f1']['d1'].text = RichTextValue(
            testText2,
            'text/plain',
            'text/html'
        )
        self.portal['f1']['d1'].reindexObject()

        import transaction
        transaction.commit()

        # Request the anonymous page again -- to test expiration of 304 and
        # RAM.
        etag = browser.headers['ETag']
        browser = Browser(self.app)
        browser.addHeader('If-None-Match', etag)
        browser.open(self.portal['f1']['d1'].absolute_url())
        self.assertEqual('plone.content.itemView',
                         browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.weakCaching',
                         browser.headers['X-Cache-Operation'])
        # The etag has changed so we should get a fresh page.
        self.assertIsNone(browser.headers.get('X-RAMCache'))
        self.assertEqual('200 OK', browser.headers['Status'].upper())

    def test_content_feeds(self):

        catalog = self.portal['portal_catalog']
        skins_tool = self.portal['portal_skins']

        # Enable syndication
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        self.syndication = getToolByName(self.portal, 'portal_syndication')
        self.syndication.editProperties(isAllowed=True)
        self.syndication.enableSyndication(self.portal)

        import transaction
        transaction.commit()

        # Request the rss feed
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal.absolute_url() + '/RSS')
        self.assertEqual('plone.content.feed', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInProxy
        self.assertEqual('max-age=0, s-maxage=86400, must-revalidate',
                         browser.headers['Cache-Control'])
        tag = '"||{0}|en|{1}"'.format(
            catalog.getCounter(),
            skins_tool.default_skin,
        )
        self.assertEqual(tag, browser.headers['ETag'])
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the rss feed again -- to test RAM cache
        now = stable_now()
        rssText = browser.contents
        browser = Browser(self.app)
        browser.open(self.portal.absolute_url() + '/RSS')
        self.assertEqual('plone.content.feed', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # This should come from the RAM cache
        self.assertEqual('plone.app.caching.operations.ramcache',
                         browser.headers['X-RAMCache'])
        self.assertEqual(rssText, browser.contents)
        self.assertEqual('max-age=0, s-maxage=86400, must-revalidate',
                         browser.headers['Cache-Control'])
        tag = '"||{0}|en|{1}"'.format(
            catalog.getCounter(),
            skins_tool.default_skin,
        )
        self.assertEqual(tag, browser.headers['ETag'])
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the rss feed again -- with an INM header to test 304.
        etag = browser.headers['ETag']
        browser = Browser(self.app)
        browser.raiseHttpErrors = False
        browser.addHeader('If-None-Match', etag)
        browser.open(self.portal.absolute_url() + '/RSS')
        self.assertEqual('plone.content.feed', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # This should be a 304 response
        self.assertEqual('304 Not Modified', browser.headers['Status'])
        self.assertEqual('', browser.contents)

        # Request the authenticated rss feed
        now = stable_now()
        browser = Browser(self.app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD, ),
        )
        browser.open(self.portal.absolute_url() + '/RSS')
        self.assertEqual('plone.content.feed', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        tag = '"|test_user_1_|{0}|en|{1}"'.format(
            catalog.getCounter(),
            skins_tool.default_skin,
        )
        self.assertEqual(tag, browser.headers['ETag'])
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the authenticated rss feed again -- to test RAM cache
        browser = Browser(self.app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD, ),
        )
        browser.open(self.portal.absolute_url() + '/RSS')
        self.assertEqual('plone.content.feed', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # Authenticated should NOT be RAM cached
        self.assertIsNone(browser.headers.get('X-RAMCache'))

    def test_content_files(self):

        # Add folder content
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        self.portal.invokeFactory('Folder', 'f1')
        self.portal['f1'].title = u"Folder one"
        self.portal['f1'].description = u"Folder one description"
        self.portal['f1'].reindexObject()

        # Add content image
        self.portal['f1'].invokeFactory('Image', 'i1')
        self.portal['f1']['i1'].title = u"Image one"
        self.portal['f1']['i1'].description = u"Image one description"
        self.portal['f1']['i1'].image = test_image()
        self.portal['f1']['i1'].reindexObject()

        import transaction
        transaction.commit()

        # Request the image with Manager role
        now = stable_now()
        browser = Browser(self.app)
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ),
        )
        browser.open(self.portal['f1']['i1'].absolute_url())
        self.assertEqual('plone.content.file', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # Folder not published yet so image should not be cached in proxy
        # so this should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        # remove this when the next line works
        self.assertIsNotNone(browser.headers.get('Last-Modified'))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request an image scale with Manager role
        now = stable_now()
        browser = Browser(self.app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ),
        )
        browser.open(self.portal['f1'][
                     'i1'].absolute_url() + '/@@images/image/preview')
        self.assertEqual('plone.content.file', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # Folder not published yet so image scale should not be cached in proxy
        # so this should use cacheInBrowser
        self.assertEqual('max-age=0, must-revalidate, private',
                         browser.headers['Cache-Control'])
        # remove this when the next line works
        self.assertIsNotNone(browser.headers.get('Last-Modified'))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Publish the folder
        self.portal.portal_workflow.doActionFor(self.portal['f1'], 'publish')

        import transaction
        transaction.commit()

        # Request the image
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal['f1']['i1'].absolute_url())
        self.assertEqual('plone.content.file', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # Now visible to anonymous so this should use cacheInProxy
        self.assertEqual('max-age=0, s-maxage=86400, must-revalidate',
                         browser.headers['Cache-Control'])
        # remove this when the next line works
        self.assertIsNotNone(browser.headers.get('Last-Modified'))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

        # Request the image again -- with an IMS header to test 304
        lastmodified = browser.headers['Last-Modified']
        browser = Browser(self.app)
        browser.raiseHttpErrors = False
        browser.addHeader('If-Modified-Since', lastmodified)
        browser.open(self.portal['f1']['i1'].absolute_url())
        self.assertEqual('plone.content.file', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # This should be a 304 response
        self.assertEqual('304 Not Modified', browser.headers['Status'])
        self.assertEqual('', browser.contents)

        # Request an image scale
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal['f1'][
                     'i1'].absolute_url() + '/@@images/image/preview')
        self.assertEqual('plone.content.file', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.moderateCaching',
                         browser.headers['X-Cache-Operation'])
        # Now visible to anonymous so this should use cacheInProxy
        self.assertEqual('max-age=0, s-maxage=86400, must-revalidate',
                         browser.headers['Cache-Control'])
        # remove this when the next line works
        self.assertIsNotNone(browser.headers.get('Last-Modified'))
        self.assertGreater(now, dateutil.parser.parse(
            browser.headers['Expires']))

    def test_resources(self):
        # This is a clone of the same test for 'without-caching-proxy'
        # Can we just call that test from this context?

        import transaction
        transaction.commit()

        # Request a skin image
        now = stable_now()
        browser = Browser(self.app)
        browser.open(self.portal.absolute_url() + '/rss.png')
        self.assertEqual('plone.resource', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.strongCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInBrowserAndProxy
        self.assertEqual('max-age=86400, proxy-revalidate, public',
                         browser.headers['Cache-Control'])
        # remove this when the next line works
        self.assertIsNotNone(browser.headers.get('Last-Modified'))
        timedelta = dateutil.parser.parse(browser.headers['Expires']) - now
        self.assertGreater(timedelta, datetime.timedelta(seconds=86390))

        # Request the skin image again -- with an IMS header to test 304
        lastmodified = browser.headers['Last-Modified']
        browser = Browser(self.app)
        browser.raiseHttpErrors = False
        browser.addHeader('If-Modified-Since', lastmodified)
        browser.open(self.portal.absolute_url() + '/rss.png')
        self.assertEqual('plone.resource', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.strongCaching',
                         browser.headers['X-Cache-Operation'])
        # This should be a 304 response
        self.assertEqual('304 Not Modified', browser.headers['Status'])
        self.assertEqual('', browser.contents)

        # Request a large datafile (over 64K) to test files that use
        # the "response.write()" function to initiate a streamed response.
        # This is of type OFS.Image.File but it should also apply to
        # large OFS.Image.Image, large non-blog ATImages/ATFiles, and
        # large Resource Registry cooked files, which all use the same
        # method to initiate a streamed response.
        s = 'a' * (1 << 16) * 3
        self.portal.manage_addFile('bigfile', file=StringIO(
            s), content_type='application/octet-stream')

        import transaction
        transaction.commit()

        browser = Browser(self.app)
        browser.open(self.portal['bigfile'].absolute_url())
        self.assertEqual('plone.resource', browser.headers['X-Cache-Rule'])
        self.assertEqual('plone.app.caching.strongCaching',
                         browser.headers['X-Cache-Operation'])
        # This should use cacheInBrowserAndProxy
        self.assertEqual('max-age=86400, proxy-revalidate, public',
                         browser.headers['Cache-Control'])
        # remove this when the next line works
        self.assertIsNotNone(browser.headers.get('Last-Modified'))
        timedelta = dateutil.parser.parse(browser.headers['Expires']) - now
        self.assertGreater(timedelta, datetime.timedelta(seconds=86390))

    def test_stable_resources(self):
        # This is a clone of the same test for 'without-caching-proxy'
        # Can we just call that test from this context?
        # (yes, this is not really testing anything. It's a placeholder)
        #
        # We don't actually have any non-RR stable resources yet
        # What is the best way to test this?
        # Maybe not important since the RR test exercises the same code?
        pass
