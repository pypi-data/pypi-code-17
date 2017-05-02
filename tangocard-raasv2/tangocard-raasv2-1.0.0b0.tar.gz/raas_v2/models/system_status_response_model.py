# -*- coding: utf-8 -*-

"""
    raas_v2.models.system_status_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class SystemStatusResponseModel(object):

    """Implementation of the 'SystemStatusResponse' model.

    System Status Response Model

    Attributes:
        status (string): System Status

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "status" : "status"
    }

    def __init__(self,
                 status=None):
        """Constructor for the SystemStatusResponseModel class"""

        # Initialize members of the class
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
        status = dictionary.get("status")

        # Return an object of this model
        return cls(status)


