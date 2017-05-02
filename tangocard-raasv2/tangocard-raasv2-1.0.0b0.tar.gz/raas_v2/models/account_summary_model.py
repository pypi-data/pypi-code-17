# -*- coding: utf-8 -*-

"""
    raas_v2.models.account_summary_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas_v2.api_helper import APIHelper

class AccountSummaryModel(object):

    """Implementation of the 'AccountSummary' model.

    Account Summary Model

    Attributes:
        account_identifier (string): Account Identifier
        display_name (string): Display Name
        created_at (datetime): Date Created
        status (string): Status

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_identifier" : "accountIdentifier",
        "display_name" : "displayName",
        "created_at" : "createdAt",
        "status" : "status"
    }

    def __init__(self,
                 account_identifier=None,
                 display_name=None,
                 created_at=None,
                 status=None):
        """Constructor for the AccountSummaryModel class"""

        # Initialize members of the class
        self.account_identifier = account_identifier
        self.display_name = display_name
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.status = status


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
        account_identifier = dictionary.get("accountIdentifier")
        display_name = dictionary.get("displayName")
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        status = dictionary.get("status")

        # Return an object of this model
        return cls(account_identifier,
                   display_name,
                   created_at,
                   status)


