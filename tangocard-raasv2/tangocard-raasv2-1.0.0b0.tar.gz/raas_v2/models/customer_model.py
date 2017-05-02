# -*- coding: utf-8 -*-

"""
    raas_v2.models.customer_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas_v2.api_helper import APIHelper
import raas_v2.models.account_summary_model

class CustomerModel(object):

    """Implementation of the 'Customer' model.

    Customer Model

    Attributes:
        customer_identifier (string): Customer Identifier
        display_name (string): Display Name
        status (string): Status
        created_at (datetime): Date Created
        accounts (list of AccountSummaryModel): Accounts

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "customer_identifier" : "customerIdentifier",
        "display_name" : "displayName",
        "status" : "status",
        "created_at" : "createdAt",
        "accounts" : "accounts"
    }

    def __init__(self,
                 customer_identifier=None,
                 display_name=None,
                 status=None,
                 created_at=None,
                 accounts=None):
        """Constructor for the CustomerModel class"""

        # Initialize members of the class
        self.customer_identifier = customer_identifier
        self.display_name = display_name
        self.status = status
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.accounts = accounts


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        customer_identifier = dictionary.get("customerIdentifier")
        display_name = dictionary.get("displayName")
        status = dictionary.get("status")
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        accounts = None
        if dictionary.get("accounts") != None:
            accounts = list()
            for structure in dictionary.get("accounts"):
                accounts.append(raas_v2.models.account_summary.AccountSummaryModel.from_dictionary(structure))

        # Return an object of this model
        return cls(customer_identifier,
                   display_name,
                   status,
                   created_at,
                   accounts)


