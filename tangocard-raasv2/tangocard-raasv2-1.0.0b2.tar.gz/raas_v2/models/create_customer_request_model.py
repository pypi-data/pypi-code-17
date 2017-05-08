# -*- coding: utf-8 -*-

"""
    raas_v2.models.create_customer_request_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class CreateCustomerRequestModel(object):

    """Implementation of the 'CreateCustomerRequest' model.

    Create Customer Request

    Attributes:
        customer_identifier (string): Customer Identifier
        display_name (string): Display Name

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "customer_identifier" : "customerIdentifier",
        "display_name" : "displayName"
    }

    def __init__(self,
                 customer_identifier=None,
                 display_name=None):
        """Constructor for the CreateCustomerRequestModel class"""

        # Initialize members of the class
        self.customer_identifier = customer_identifier
        self.display_name = display_name


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

        # Return an object of this model
        return cls(customer_identifier,
                   display_name)


