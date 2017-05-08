# -*- coding: utf-8 -*-

"""
    raas_v2.controllers.accounts_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.basic_auth import BasicAuth
from ..models.account_summary_model import AccountSummaryModel
from ..models.account_model import AccountModel

class AccountsController(BaseController):

    """A Controller to access Endpoints in the raas_v2 API."""

    def __init__(self, client=None, call_back=None):
        super(AccountsController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def get_accounts_by_customer(self,
                                 customer_identifier):
        """Does a GET request to /customers/{customerIdentifier}/accounts.

        Gets a list of accounts for a given customer

        Args:
            customer_identifier (string): Customer Identifier

        Returns:
            list of AccountSummaryModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_accounts_by_customer called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_accounts_by_customer.')
            self.validate_parameters(customer_identifier=customer_identifier)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_accounts_by_customer.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/customers/{customerIdentifier}/accounts'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'customerIdentifier': customer_identifier
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_accounts_by_customer.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_accounts_by_customer.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_accounts_by_customer')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, AccountSummaryModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_account(self,
                    account_identifier):
        """Does a GET request to /accounts/{accountIdentifier}.

        Get an account

        Args:
            account_identifier (string): Account Identifier

        Returns:
            AccountModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_account called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_account.')
            self.validate_parameters(account_identifier=account_identifier)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_account.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/accounts/{accountIdentifier}'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'accountIdentifier': account_identifier
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_account.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_account.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_account')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, AccountModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def create_account(self,
                       customer_identifier,
                       body):
        """Does a POST request to /customers/{customerIdentifier}/accounts.

        Create an account under a given customer

        Args:
            customer_identifier (string): Customer Identifier
            body (CreateAccountRequestModel): Request Body

        Returns:
            AccountModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_account called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for create_account.')
            self.validate_parameters(customer_identifier=customer_identifier,
                                     body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_account.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/customers/{customerIdentifier}/accounts'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'customerIdentifier': customer_identifier
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_account.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_account.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'create_account')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, AccountModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_all_accounts(self):
        """Does a GET request to /accounts.

        Gets all accounts under the platform

        Returns:
            list of AccountModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_all_accounts called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_all_accounts.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/accounts'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_all_accounts.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_all_accounts.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_all_accounts')
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, AccountModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
