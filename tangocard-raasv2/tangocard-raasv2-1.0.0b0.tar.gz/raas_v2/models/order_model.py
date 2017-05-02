# -*- coding: utf-8 -*-

"""
    raas_v2.models.order_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas_v2.api_helper import APIHelper
import raas_v2.models.currency_breakdown_model
import raas_v2.models.reward_model
import raas_v2.models.name_email_model

class OrderModel(object):

    """Implementation of the 'Order' model.

    Order Model

    Attributes:
        account_identifier (string): Account Identifier
        amount_charged (CurrencyBreakdownModel): Amount Charged
        created_at (datetime): Created At
        customer_identifier (string): Customer Identifier
        denomination (CurrencyBreakdownModel): Denomination
        reference_order_id (string): Reference Order ID
        reward (RewardModel): Reward
        reward_name (string): Reward Name
        send_email (bool): Send Email
        status (string): Status
        utid (string): UTID
        campaign (string): Campaign
        email_subject (string): Email Subject
        external_ref_id (string): External Reference ID
        message (string): Message
        notes (string): Notes
        recipient (NameEmailModel): Recipient
        sender (NameEmailModel): Sender

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_identifier" : "accountIdentifier",
        "amount_charged" : "amountCharged",
        "created_at" : "createdAt",
        "customer_identifier" : "customerIdentifier",
        "denomination" : "denomination",
        "reference_order_id" : "referenceOrderID",
        "reward" : "reward",
        "reward_name" : "rewardName",
        "send_email" : "sendEmail",
        "status" : "status",
        "utid" : "utid",
        "campaign" : "campaign",
        "email_subject" : "emailSubject",
        "external_ref_id" : "externalRefID",
        "message" : "message",
        "notes" : "notes",
        "recipient" : "recipient",
        "sender" : "sender"
    }

    def __init__(self,
                 account_identifier=None,
                 amount_charged=None,
                 created_at=None,
                 customer_identifier=None,
                 denomination=None,
                 reference_order_id=None,
                 reward=None,
                 reward_name=None,
                 send_email=None,
                 status=None,
                 utid=None,
                 campaign=None,
                 email_subject=None,
                 external_ref_id=None,
                 message=None,
                 notes=None,
                 recipient=None,
                 sender=None):
        """Constructor for the OrderModel class"""

        # Initialize members of the class
        self.account_identifier = account_identifier
        self.amount_charged = amount_charged
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.customer_identifier = customer_identifier
        self.denomination = denomination
        self.reference_order_id = reference_order_id
        self.reward = reward
        self.reward_name = reward_name
        self.send_email = send_email
        self.status = status
        self.utid = utid
        self.campaign = campaign
        self.email_subject = email_subject
        self.external_ref_id = external_ref_id
        self.message = message
        self.notes = notes
        self.recipient = recipient
        self.sender = sender


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
        account_identifier = dictionary.get("accountIdentifier")
        amount_charged = raas_v2.models.currency_breakdown_model.CurrencyBreakdownModel.from_dictionary(dictionary.get("amountCharged")) if dictionary.get("amountCharged") else None
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        customer_identifier = dictionary.get("customerIdentifier")
        denomination = raas_v2.models.currency_breakdown_model.CurrencyBreakdownModel.from_dictionary(dictionary.get("denomination")) if dictionary.get("denomination") else None
        reference_order_id = dictionary.get("referenceOrderID")
        reward = raas_v2.models.reward_model.RewardModel.from_dictionary(dictionary.get("reward")) if dictionary.get("reward") else None
        reward_name = dictionary.get("rewardName")
        send_email = dictionary.get("sendEmail")
        status = dictionary.get("status")
        utid = dictionary.get("utid")
        campaign = dictionary.get("campaign")
        email_subject = dictionary.get("emailSubject")
        external_ref_id = dictionary.get("externalRefID")
        message = dictionary.get("message")
        notes = dictionary.get("notes")
        recipient = raas_v2.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get("recipient")) if dictionary.get("recipient") else None
        sender = raas_v2.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get("sender")) if dictionary.get("sender") else None

        # Return an object of this model
        return cls(account_identifier,
                   amount_charged,
                   created_at,
                   customer_identifier,
                   denomination,
                   reference_order_id,
                   reward,
                   reward_name,
                   send_email,
                   status,
                   utid,
                   campaign,
                   email_subject,
                   external_ref_id,
                   message,
                   notes,
                   recipient,
                   sender)


