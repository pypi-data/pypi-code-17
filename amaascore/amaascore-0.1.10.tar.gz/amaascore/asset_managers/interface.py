from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from amaascore.asset_managers.utils import json_to_asset_manager
from amaascore.config import ENDPOINTS
from amaascore.core.interface import Interface


class AssetManagersInterface(Interface):
    """
    The interface to the Asset Managers service for reading Asset Manager information.
    """

    def __init__(self, logger=None):
        endpoint = ENDPOINTS.get('asset_managers')
        self.logger = logger or logging.getLogger(__name__)
        super(AssetManagersInterface, self).__init__(endpoint=endpoint)

    def new(self, asset_manager):
        self.logger.info('New Asset Manager: %s', asset_manager.asset_manager_id)
        url = '%s/asset_managers' % self.endpoint
        response = self.session.post(url, json=asset_manager.to_interface())
        if response.ok:
            self.logger.info('Successfully Created Asset Manager: %s', asset_manager.asset_manager_id)
            return json_to_asset_manager(response.json())
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve(self, asset_manager_id):
        self.logger.info('Retrieve Asset Manager: %s', asset_manager_id)
        url = '%s/asset_managers/%s' % (self.endpoint, asset_manager_id)
        response = self.session.get(url)
        if response.ok:
            self.logger.info('Successfully Retrieved Asset Manager: %s', asset_manager_id)
            return json_to_asset_manager(response.json())
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def deactivate(self, asset_manager_id):
        """
        Is is only possible to deactivate an asset manager if your client_id is also the client_id that was used
        to originally create the asset manager.

        :param asset_manager_id:
        :return:
        """
        self.logger.info('Deactivate Asset Manager: %s', asset_manager_id)
        url = '%s/asset_managers/%s' % (self.endpoint, asset_manager_id)
        response = self.session.delete(url)
        if response.ok:
            self.logger.info('Successfully deactivated Asset Manager: %s', asset_manager_id)
            return json_to_asset_manager(response.json())
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def search(self, asset_manager_ids=None, client_ids=None):
        self.logger.info('Search for Asset Managers: %s', asset_manager_ids)
        search_params = {}
        # Potentially roll this into a loop through args rather than explicitly named - depends on additional validation
        if asset_manager_ids:
            search_params['asset_manager_ids'] = asset_manager_ids
        if client_ids:
            search_params['client_ids'] = client_ids
        url = self.endpoint + '/asset_managers'
        response = self.session.get(url, params=search_params)
        if response.ok:
            asset_managers = [json_to_asset_manager(json_asset_manager) for json_asset_manager in response.json()]
            self.logger.info('Returned %s Asset Managers.', len(asset_managers))
            return asset_managers
        else:
            self.logger.error(response.text)
            response.raise_for_status()


