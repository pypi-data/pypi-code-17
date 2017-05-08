# -*- coding: utf-8 -*-

"""
    raas_v2.models.reward_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas_v2.models.reward_credential_model

class RewardModel(object):

    """Implementation of the 'Reward' model.

    Reward Model

    Attributes:
        credentials (dict<object, string>): A map of reward credentials
        credential_list (list of RewardCredentialModel): An array of reward
            credentials
        redemption_instructions (string): Reward redemption instructions

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "credentials" : "credentials",
        "credential_list" : "credentialList",
        "redemption_instructions" : "redemptionInstructions"
    }

    def __init__(self,
                 credentials=None,
                 credential_list=None,
                 redemption_instructions=None):
        """Constructor for the RewardModel class"""

        # Initialize members of the class
        self.credentials = credentials
        self.credential_list = credential_list
        self.redemption_instructions = redemption_instructions


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
        credentials = dictionary.get("credentials")
        credential_list = None
        if dictionary.get("credentialList") != None:
            credential_list = list()
            for structure in dictionary.get("credentialList"):
                credential_list.append(raas_v2.models.reward_credential_model.RewardCredentialModel.from_dictionary(structure))
        redemption_instructions = dictionary.get("redemptionInstructions")

        # Return an object of this model
        return cls(credentials,
                   credential_list,
                   redemption_instructions)


