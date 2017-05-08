# -*- coding: utf-8 -*-

"""
    raas_v2.models.exchange_rate_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas_v2.models.exchange_rate_model

class ExchangeRateResponseModel(object):

    """Implementation of the 'ExchangeRateResponse' model.

    Exchange Rate Response Model

    Attributes:
        disclaimer (string): Disclaimer
        exchange_rates (list of ExchangeRateModel): Exchange Rates

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "disclaimer" : "disclaimer",
        "exchange_rates" : "exchangeRates"
    }

    def __init__(self,
                 disclaimer=None,
                 exchange_rates=None):
        """Constructor for the ExchangeRateResponseModel class"""

        # Initialize members of the class
        self.disclaimer = disclaimer
        self.exchange_rates = exchange_rates


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
        disclaimer = dictionary.get("disclaimer")
        exchange_rates = None
        if dictionary.get("exchangeRates") != None:
            exchange_rates = list()
            for structure in dictionary.get("exchangeRates"):
                exchange_rates.append(raas_v2.models.exchange_rate_model.ExchangeRateModel.from_dictionary(structure))

        # Return an object of this model
        return cls(disclaimer,
                   exchange_rates)


