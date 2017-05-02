# -*- coding: utf-8 -*-

"""
    raas_v2.models.item_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas_v2.api_helper import APIHelper

class ItemModel(object):

    """Implementation of the 'Item' model.

    Item Model

    Attributes:
        utid (string): UTID
        reward_name (string): Reward Name
        currency_code (string): Currency Code
        status (string): Status
        value_type (string): Value Type (fixed/variable)
        reward_type (string): Reward Type
        created_date (datetime): Date Created
        last_update_date (datetime): Last Updated
        countries (list of string): Countries
        min_value (float): Minimum Value (for variable value items)
        max_value (float): Maximum Value (for variable value items)
        face_value (float): Face Value

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "utid" : "utid",
        "reward_name" : "rewardName",
        "currency_code" : "currencyCode",
        "status" : "status",
        "value_type" : "valueType",
        "reward_type" : "rewardType",
        "created_date" : "createdDate",
        "last_update_date" : "lastUpdateDate",
        "countries" : "countries",
        "min_value" : "minValue",
        "max_value" : "maxValue",
        "face_value" : "faceValue"
    }

    def __init__(self,
                 utid=None,
                 reward_name=None,
                 currency_code=None,
                 status=None,
                 value_type=None,
                 reward_type=None,
                 created_date=None,
                 last_update_date=None,
                 countries=None,
                 min_value=None,
                 max_value=None,
                 face_value=None):
        """Constructor for the ItemModel class"""

        # Initialize members of the class
        self.utid = utid
        self.reward_name = reward_name
        self.currency_code = currency_code
        self.status = status
        self.value_type = value_type
        self.reward_type = reward_type
        self.created_date = APIHelper.RFC3339DateTime(created_date) if created_date else None
        self.last_update_date = APIHelper.RFC3339DateTime(last_update_date) if last_update_date else None
        self.countries = countries
        self.min_value = min_value
        self.max_value = max_value
        self.face_value = face_value


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
        utid = dictionary.get("utid")
        reward_name = dictionary.get("rewardName")
        currency_code = dictionary.get("currencyCode")
        status = dictionary.get("status")
        value_type = dictionary.get("valueType")
        reward_type = dictionary.get("rewardType")
        created_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdDate")).datetime if dictionary.get("createdDate") else None
        last_update_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("lastUpdateDate")).datetime if dictionary.get("lastUpdateDate") else None
        countries = dictionary.get("countries")
        min_value = dictionary.get("minValue")
        max_value = dictionary.get("maxValue")
        face_value = dictionary.get("faceValue")

        # Return an object of this model
        return cls(utid,
                   reward_name,
                   currency_code,
                   status,
                   value_type,
                   reward_type,
                   created_date,
                   last_update_date,
                   countries,
                   min_value,
                   max_value,
                   face_value)


