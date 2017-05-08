# -*- coding: utf-8 -*-

"""
    raas_v2.controllers.orders_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.basic_auth import BasicAuth
from ..models.order_model import OrderModel
from ..models.resend_order_response_model import ResendOrderResponseModel
from ..models.get_orders_response_model import GetOrdersResponseModel

class OrdersController(BaseController):

    """A Controller to access Endpoints in the raas_v2 API."""

    def __init__(self, client=None, call_back=None):
        super(OrdersController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def create_order(self,
                     body):
        """Does a POST request to /orders.

        TODO: type endpoint description here.

        Args:
            body (CreateOrderRequestModel): TODO: type description here.
                Example: 

        Returns:
            OrderModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_order called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for create_order.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_order.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/orders'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_order.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_order.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'create_order')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, OrderModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_order(self,
                  reference_order_id):
        """Does a GET request to /orders/{referenceOrderID}.

        TODO: type endpoint description here.

        Args:
            reference_order_id (string): Reference Order ID

        Returns:
            OrderModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_order called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_order.')
            self.validate_parameters(reference_order_id=reference_order_id)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_order.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/orders/{referenceOrderID}'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'referenceOrderID': reference_order_id
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_order.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_order.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_order')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, OrderModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def create_resend_order(self,
                            reference_order_id):
        """Does a POST request to /orders/{referenceOrderID}/resends.

        TODO: type endpoint description here.

        Args:
            reference_order_id (string): TODO: type description here. Example:
                
        Returns:
            ResendOrderResponseModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_resend_order called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for create_resend_order.')
            self.validate_parameters(reference_order_id=reference_order_id)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_resend_order.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/orders/{referenceOrderID}/resends'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'referenceOrderID': reference_order_id
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_resend_order.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_resend_order.')
            _request = self.http_client.post(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'create_resend_order')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ResendOrderResponseModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_orders(self,
                   options=dict()):
        """Does a GET request to /orders.

        TODO: type endpoint description here.

        Args:
            options (dict, optional): Key-value pairs for any of the
                parameters to this API Endpoint. All parameters to the
                endpoint are supplied through the dictionary with their names
                being the key and their desired values being the value. A list
                of parameters that can be used are::

                    account_identifier -- string -- TODO: type description
                        here. Example: 
                    customer_identifier -- string -- TODO: type description
                        here. Example: 
                    external_ref_id -- string -- TODO: type description here.
                        Example: 
                    start_date -- datetime -- TODO: type description here.
                        Example: 
                    end_date -- datetime -- TODO: type description here.
                        Example: 
                    elements_per_block -- int -- TODO: type description here.
                        Example: 
                    page -- int -- TODO: type description here. Example: 

        Returns:
            GetOrdersResponseModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_orders called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_orders.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/orders'
            _query_url = APIHelper.clean_url(_query_builder)
            _query_parameters = {
                'accountIdentifier': options.get('account_identifier', None),
                'customerIdentifier': options.get('customer_identifier', None),
                'externalRefID': options.get('external_ref_id', None),
                'startDate': APIHelper.RFC3339DateTime(options.get('start_date', None)),
                'endDate': APIHelper.RFC3339DateTime(options.get('end_date', None)),
                'elementsPerBlock': options.get('elements_per_block', None),
                'page': options.get('page', None)
            }
    
            # Prepare headers
            self.logger.info('Preparing headers for get_orders.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_orders.')
            _request = self.http_client.get(_query_url, headers=_headers, query_parameters=_query_parameters)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_orders')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, GetOrdersResponseModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
