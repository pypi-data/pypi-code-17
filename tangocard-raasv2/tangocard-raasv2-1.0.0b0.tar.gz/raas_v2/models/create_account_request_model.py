# -*- coding: utf-8 -*-

"""
    raas_v2.models.create_account_request_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class CreateAccountRequestModel(object):

    """Implementation of the 'CreateAccountRequest' model.

    Create Account Request

    Attributes:
        account_identifier (string): Account Identifier
        display_name (string): Display Name
        contact_email (string): Contact Email

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_identifier" : "accountIdentifier",
        "display_name" : "displayName",
        "contact_email" : "contactEmail"
    }

    def __init__(self,
                 account_identifier=None,
                 display_name=None,
                 contact_email=None):
        """Constructor for the CreateAccountRequestModel class"""

        # Initialize members of the class
        self.account_identifier = account_identifier
        self.display_name = display_name
        self.contact_email = contact_email


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
        contact_email = dictionary.get("contactEmail")

        # Return an object of this model
        return cls(account_identifier,
                   display_name,
                   contact_email)


