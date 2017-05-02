# -*- coding: utf-8 -*-

"""
    raas_v2.models.name_email_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class NameEmailModel(object):

    """Implementation of the 'NameEmail' model.

    Name and Email Model

    Attributes:
        email (string): Email Address
        first_name (string): First Name
        last_name (string): Last Name

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email" : "email",
        "first_name" : "firstName",
        "last_name" : "lastName"
    }

    def __init__(self,
                 email=None,
                 first_name=None,
                 last_name=None):
        """Constructor for the NameEmailModel class"""

        # Initialize members of the class
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


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
        email = dictionary.get("email")
        first_name = dictionary.get("firstName")
        last_name = dictionary.get("lastName")

        # Return an object of this model
        return cls(email,
                   first_name,
                   last_name)


