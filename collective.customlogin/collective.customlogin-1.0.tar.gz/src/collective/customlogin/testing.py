from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class CollectivecustomloginLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.customlogin
        xmlconfig.file(
            'configure.zcml',
            collective.customlogin,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')


COLLECTIVE_CUSTOMLOGIN_FIXTURE = CollectivecustomloginLayer()
COLLECTIVE_CUSTOMLOGIN_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CUSTOMLOGIN_FIXTURE,),
    name="CollectivecustomloginLayer:Integration"
)
COLLECTIVE_CUSTOMLOGIN_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CUSTOMLOGIN_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectivecustomloginLayer:Functional"
)
