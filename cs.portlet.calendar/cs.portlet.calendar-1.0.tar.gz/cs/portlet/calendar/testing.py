# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import quickInstallProduct
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from zope.configuration import xmlconfig
import collective.MockMailHost


class CSPortletCalendarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import cs.portlet.calendar
        xmlconfig.file(
            'configure.zcml',
            cs.portlet.calendar,
            context=configurationContext
        )

        self.loadZCML(package=collective.MockMailHost)
        z2.installProduct(app, 'cs.portlet.calendar')

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ['Manager'], [])
        login(portal, SITE_OWNER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        applyProfile(portal, 'cs.portlet.calendar:default')
        quickInstallProduct(portal, 'collective.MockMailHost')
        applyProfile(portal, 'collective.MockMailHost:default')


CS_PORTLET_CALENDAR_FIXTURE = CSPortletCalendarLayer()
CS_PORTLET_CALENDAR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CS_PORTLET_CALENDAR_FIXTURE,),
    name="CSPortletCalendarLayer:Integration"
)
CS_PORTLET_CALENDAR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CS_PORTLET_CALENDAR_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CSPortletCalendarLayer:Functional"
)
