# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.eeatags.collection.testing import COLLECTIVE_EEATAGS_COLLECTION_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.eeatags.collection is properly installed."""

    layer = COLLECTIVE_EEATAGS_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.eeatags.collection is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.eeatags.collection'))

    def test_eeatags_installed(self):
        """Test if eea.tags is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'eea.tags'))

    def test_browserlayer(self):
        """Test that ICollectiveEeatagsCollectionLayer is registered."""
        from collective.eeatags.collection.interfaces import (
            ICollectiveEeatagsCollectionLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveEeatagsCollectionLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_EEATAGS_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.eeatags.collection'])

    def test_product_uninstalled(self):
        """Test if collective.eeatags.collection is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.eeatags.collection'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEeatagsCollectionLayer is removed."""
        from collective.eeatags.collection.interfaces import \
            ICollectiveEeatagsCollectionLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveEeatagsCollectionLayer, utils.registered_layers())
