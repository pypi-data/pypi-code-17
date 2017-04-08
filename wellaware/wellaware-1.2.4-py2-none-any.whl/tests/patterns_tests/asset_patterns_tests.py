from __future__ import unicode_literals

from wellaware._compat import array_types
from wellaware.client import Asset, Assets, Token, AssetPatterns, Point, DataRetrieveResponse, Observation
from wellaware.tests.base import *


class AssetPatternsTests(BaseClientTestCase):

    token = Token(WA_ADMIN_TOKEN)

    @attr('unit', 'assets', 'patterns')
    @responses.activate
    def test_asset_retrieve_data(self):
        # GET /assets?assetType=TANK
        asset = Asset(name='Test Asset', timezone='America/Chicago', asset_type='TANK')
        resp = [{'name': 'Test Asset', 'timezone': 'America/Chicago', 'assetType': 'TANK', 'id': 10}]
        responses.add(responses.GET, 'http://localhost/assets?assetType=TANK', json=resp, status=200,
                      match_querystring=True)

        # GET /sites/0/assets/<asset.id>/points
        point = Point(name='Test Point', timezone='America/Chicago', point_type='TOP_GAUGE')
        resp = [{'name': 'Test Point', 'timezone': 'America/Chicago', 'point_type': 'TOP_GAUGE', 'id': 11}]
        responses.add(responses.GET, 'http://localhost/sites/0/assets/10/points', json=resp, status=200,
                      match_querystring=True)

        # POST /data/retrieve
        resp = {'errors': [
        ], 'observations': {
            '11': [{'timestamp': 12345, 'value': 'test'}]
        }}
        responses.add(responses.POST, 'http://localhost/data/retrieve?start=0&end=100000', json=resp, status=200,
                      match_querystring=True)

        data = AssetPatterns.retrieve_data(self.token, asset_id=10, start=0, end=100000)
        self.assertIsInstance(data, DataRetrieveResponse)
        self.assertEquals(1, len(data.observations))
        self.assertIsInstance(data.observations[11][0], Observation)
        o = data.observations[11][0]
        self.assertEquals(12345, o.timestamp)
        self.assertEquals('test', o.value)

    @attr('unit', 'assets', 'patterns')
    @responses.activate
    def test_find_assets_by_asset_type(self):
        asset = Asset(name='Test Asset', timezone='America/Chicago', asset_type='TANK')
        resp = [{'name': 'Test Asset', 'timezone': 'America/Chicago', 'assetType': 'TANK', 'id': 10}]
        responses.add(responses.GET, 'http://localhost/assets?assetType=TANK', json=resp, status=200,
                      match_querystring=True)

        al = AssetPatterns.find_assets_by_asset_type(self.token, asset_type_filter=asset.asset_type)
        self.assertIsInstance(al, array_types)
        self.assertEqual(1, len(al))
        a = al[0]
        self.assertIsInstance(a, Asset)
        self.assertEquals(asset.name, a.name)
        self.assertEquals(asset.timezone, a.timezone)
        self.assertEquals(asset.asset_type, a.asset_type)
        self.assertEquals(10, a.id)