# -*- coding: utf-8 -*-

"""
    raas_v2.models.get_orders_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas_v2.models.page_model
import raas_v2.models.order_model

class GetOrdersResponseModel(object):

    """Implementation of the 'GetOrdersResponse' model.

    Get Orders Response

    Attributes:
        page (PageModel): Pagination information
        orders (list of OrderModel): An array of orders

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "page" : "page",
        "orders" : "orders"
    }

    def __init__(self,
                 page=None,
                 orders=None):
        """Constructor for the GetOrdersResponseModel class"""

        # Initialize members of the class
        self.page = page
        self.orders = orders


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
        page = raas_v2.models.page_model.PageModel.from_dictionary(dictionary.get("page")) if dictionary.get("page") else None
        orders = None
        if dictionary.get("orders") != None:
            orders = list()
            for structure in dictionary.get("orders"):
                orders.append(raas_v2.models.order_model.OrderModel.from_dictionary(structure))

        # Return an object of this model
        return cls(page,
                   orders)


