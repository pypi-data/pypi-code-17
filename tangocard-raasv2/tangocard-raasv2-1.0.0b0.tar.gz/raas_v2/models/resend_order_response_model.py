# -*- coding: utf-8 -*-

"""
    raas_v2.models.resend_order_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas_v2.api_helper import APIHelper

class ResendOrderResponseModel(object):

    """Implementation of the 'ResendOrderResponse' model.

    Response for Resend Order Call

    Attributes:
        created_at (datetime): When the resend request was created
        id (int): The order resend id

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "created_at" : "createdAt",
        "id" : "id"
    }

    def __init__(self,
                 created_at=None,
                 id=None):
        """Constructor for the ResendOrderResponseModel class"""

        # Initialize members of the class
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.id = id


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
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        id = dictionary.get("id")

        # Return an object of this model
        return cls(created_at,
                   id)


