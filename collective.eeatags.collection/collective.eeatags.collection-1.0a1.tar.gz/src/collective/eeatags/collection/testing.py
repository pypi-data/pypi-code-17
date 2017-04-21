# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.eeatags.collection


class CollectiveEeatagsCollectionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.eeatags.collection)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.eeatags.collection:default')


COLLECTIVE_EEATAGS_COLLECTION_FIXTURE = CollectiveEeatagsCollectionLayer()


COLLECTIVE_EEATAGS_COLLECTION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EEATAGS_COLLECTION_FIXTURE,),
    name='CollectiveEeatagsCollectionLayer:IntegrationTesting'
)


COLLECTIVE_EEATAGS_COLLECTION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EEATAGS_COLLECTION_FIXTURE,),
    name='CollectiveEeatagsCollectionLayer:FunctionalTesting'
)


COLLECTIVE_EEATAGS_COLLECTION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_EEATAGS_COLLECTION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveEeatagsCollectionLayer:AcceptanceTesting'
)
