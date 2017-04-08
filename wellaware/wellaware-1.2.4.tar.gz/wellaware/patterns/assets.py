from __future__ import unicode_literals

from wellaware.constants import make_headers
from wellaware.base.base_entity import json_collection_to_entity_collection
from wellaware.base.base_resource import BaseResource
from wellaware.resources.assets import Asset
from wellaware.resources.points.resource import Points
from wellaware.resources.data.resource import Data


class AssetPatterns(BaseResource):

    @classmethod
    def endpoint(cls):
        return '/assets'

    @classmethod
    def retrieve_data(cls, token, asset_id, start=None, end=None, limit=None, offset=None, order=None, parameters={}):
        asset_id = cls.get_entity_id(asset_id, Asset)

        points = Points.retrieve_all(token=token, site_id=0, asset_id=asset_id, parameters=parameters)
        point_ids = [point.id for point in points]

        return Data.retrieve_data(
            token=token, point_ids=point_ids, start=start, end=end, limit=limit, offset=offset, order=order,
            parameters=parameters
        )

    @classmethod
    def find_assets_by_asset_type(cls, token, asset_type_filter, parameters={}):
        if asset_type_filter is not None:
            parameters['assetType'] = asset_type_filter

        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint()), headers=make_headers(token), params=parameters)
        cls.REST_CLIENT.handle_response(response=response)

        return json_collection_to_entity_collection(response.json(), Asset)

__all__ = ['AssetPatterns']
