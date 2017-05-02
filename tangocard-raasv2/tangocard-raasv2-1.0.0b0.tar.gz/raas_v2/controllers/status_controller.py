# -*- coding: utf-8 -*-

"""
    raas_v2.controllers.status_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.basic_auth import BasicAuth
from ..models.system_status_response_model import SystemStatusResponseModel

class StatusController(BaseController):

    """A Controller to access Endpoints in the raas_v2 API."""

    def __init__(self, client=None, call_back=None):
        super(StatusController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def get_system_status(self):
        """Does a GET request to /pulse.

        Retrieve system status

        Returns:
            SystemStatusResponseModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_system_status called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_system_status.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/pulse'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_system_status.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_system_status.')
            _request = self.http_client.get(_query_url, headers=_headers)
            _context = self.execute_request(_request, name = 'get_system_status')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, SystemStatusResponseModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
