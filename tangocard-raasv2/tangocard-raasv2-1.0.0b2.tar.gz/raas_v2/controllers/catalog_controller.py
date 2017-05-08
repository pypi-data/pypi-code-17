# -*- coding: utf-8 -*-

"""
    raas_v2.controllers.catalog_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.basic_auth import BasicAuth
from ..models.catalog_model import CatalogModel

class CatalogController(BaseController):

    """A Controller to access Endpoints in the raas_v2 API."""

    def __init__(self, client=None, call_back=None):
        super(CatalogController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def get_catalog(self):
        """Does a GET request to /catalogs.

        Get Catalog

        Returns:
            CatalogModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_catalog called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_catalog.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/catalogs'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_catalog.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_catalog.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_catalog')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CatalogModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
