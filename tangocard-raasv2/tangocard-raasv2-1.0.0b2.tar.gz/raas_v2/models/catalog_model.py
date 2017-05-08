# -*- coding: utf-8 -*-

"""
    raas_v2.models.catalog_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas_v2.models.brand_model

class CatalogModel(object):

    """Implementation of the 'Catalog' model.

    Catalog Model

    Attributes:
        catalog_name (string): The name of your catalog
        brands (list of BrandModel): The brands in your catalog

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "catalog_name" : "catalogName",
        "brands" : "brands"
    }

    def __init__(self,
                 catalog_name=None,
                 brands=None):
        """Constructor for the CatalogModel class"""

        # Initialize members of the class
        self.catalog_name = catalog_name
        self.brands = brands


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
        catalog_name = dictionary.get("catalogName")
        brands = None
        if dictionary.get("brands") != None:
            brands = list()
            for structure in dictionary.get("brands"):
                brands.append(raas_v2.models.brand_model.BrandModel.from_dictionary(structure))

        # Return an object of this model
        return cls(catalog_name,
                   brands)


