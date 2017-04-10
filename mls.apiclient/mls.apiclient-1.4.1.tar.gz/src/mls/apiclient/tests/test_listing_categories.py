# -*- coding: utf-8 -*-
"""Test Propertyshelf MLS listings API."""

# python imports
import responses

# local imports
from mls.apiclient.client import ListingResource
from mls.apiclient.tests import base, utils


class TestCategories(base.BaseTestCase):
    """Listing categories test case."""
    PATH = '/api/listings/categories'

    def setUp(self):
        responses.start()

    def tearDown(self):
        responses.stop()
        responses.reset()

    def test_listing_types(self):
        resource = 'listing_types'
        responses.add(
            responses.GET,
            utils.get_url(self.URL, resource),
            body=utils.load_fixture('category_listing_types_en.json')
        )
        client = ListingResource(self.BASE_URL)
        category = client.category(resource)
        expected = [
            ('ll', 'Land Listing'),
            ('rl', 'Residential Lease'),
            ('rs', 'Residential Sale'),
        ]
        assert category == expected

    def test_view_types(self):
        resource = 'view_types'
        responses.add(
            responses.GET,
            utils.get_url(self.URL, resource),
            body=utils.load_fixture('category_view_types_en.json')
        )
        client = ListingResource(self.BASE_URL)
        category = client.category(resource)
        expected = [
            ('beach_view', 'Beach View'),
        ]
        assert category == expected
