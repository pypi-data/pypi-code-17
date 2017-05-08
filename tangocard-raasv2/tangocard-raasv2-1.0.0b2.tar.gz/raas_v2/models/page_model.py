# -*- coding: utf-8 -*-

"""
    raas_v2.models.page_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class PageModel(object):

    """Implementation of the 'Page' model.

    Model for pagination information

    Attributes:
        number (int): Page Number
        elements_per_block (int): Elements per page
        result_count (int): Result Count
        total_count (int): Total Count

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "number" : "number",
        "elements_per_block" : "elementsPerBlock",
        "result_count" : "resultCount",
        "total_count" : "totalCount"
    }

    def __init__(self,
                 number=None,
                 elements_per_block=None,
                 result_count=None,
                 total_count=None):
        """Constructor for the PageModel class"""

        # Initialize members of the class
        self.number = number
        self.elements_per_block = elements_per_block
        self.result_count = result_count
        self.total_count = total_count


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
        number = dictionary.get("number")
        elements_per_block = dictionary.get("elementsPerBlock")
        result_count = dictionary.get("resultCount")
        total_count = dictionary.get("totalCount")

        # Return an object of this model
        return cls(number,
                   elements_per_block,
                   result_count,
                   total_count)


