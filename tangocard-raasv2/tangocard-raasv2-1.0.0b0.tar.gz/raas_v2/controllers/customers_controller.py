# -*- coding: utf-8 -*-

"""
    raas_v2.controllers.customers_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.basic_auth import BasicAuth
from ..models.customer_model import CustomerModel

class CustomersController(BaseController):

    """A Controller to access Endpoints in the raas_v2 API."""

    def __init__(self, client=None, call_back=None):
        super(CustomersController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def get_customer(self,
                     customer_identifier):
        """Does a GET request to /customers/{customerIdentifier}.

        Get a customer

        Args:
            customer_identifier (string): Customer Identifier

        Returns:
            CustomerModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_customer called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_customer.')
            self.validate_parameters(customer_identifier=customer_identifier)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_customer.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/customers/{customerIdentifier}'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'customerIdentifier': customer_identifier
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_customer.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_customer.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_customer')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CustomerModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def create_customer(self,
                        body):
        """Does a POST request to /customers.

        Create a new customer

        Args:
            body (CreateCustomerRequestModel): Request Body

        Returns:
            CustomerModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_customer called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for create_customer.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_customer.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/customers'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_customer.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_customer.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'create_customer')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CustomerModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_all_customers(self):
        """Does a GET request to /customers.

        Gets all customers under the platform

        Returns:
            list of CustomerModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_all_customers called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_all_customers.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/customers'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_all_customers.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_all_customers.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_all_customers')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CustomerModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
