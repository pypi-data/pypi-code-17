# -*- coding: utf-8 -*-

"""
    raas_v2.models.create_order_request_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas_v2.models.name_email_model

class CreateOrderRequestModel(object):

    """Implementation of the 'CreateOrderRequest' model.

    Create Order Request

    Attributes:
        account_identifier (string): Account Identifier
        amount (float): Amount
        customer_identifier (string): Customer Identifier
        send_email (bool): Send Email
        utid (string): UTID
        campaign (string): Campaign
        email_subject (string): Email Subject
        external_ref_id (string): External Reference ID
        message (string): Email Message
        recipient (NameEmailModel): Recipient
        sender (NameEmailModel): Sender
        notes (string): Notes

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_identifier" : "accountIdentifier",
        "amount" : "amount",
        "customer_identifier" : "customerIdentifier",
        "send_email" : "sendEmail",
        "utid" : "utid",
        "campaign" : "campaign",
        "email_subject" : "emailSubject",
        "external_ref_id" : "externalRefID",
        "message" : "message",
        "recipient" : "recipient",
        "sender" : "sender",
        "notes" : "notes"
    }

    def __init__(self,
                 account_identifier=None,
                 amount=None,
                 customer_identifier=None,
                 send_email=None,
                 utid=None,
                 campaign=None,
                 email_subject=None,
                 external_ref_id=None,
                 message=None,
                 recipient=None,
                 sender=None,
                 notes=None):
        """Constructor for the CreateOrderRequestModel class"""

        # Initialize members of the class
        self.account_identifier = account_identifier
        self.amount = amount
        self.customer_identifier = customer_identifier
        self.send_email = send_email
        self.utid = utid
        self.campaign = campaign
        self.email_subject = email_subject
        self.external_ref_id = external_ref_id
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.notes = notes


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
        amount = dictionary.get("amount")
        customer_identifier = dictionary.get("customerIdentifier")
        send_email = dictionary.get("sendEmail")
        utid = dictionary.get("utid")
        campaign = dictionary.get("campaign")
        email_subject = dictionary.get("emailSubject")
        external_ref_id = dictionary.get("externalRefID")
        message = dictionary.get("message")
        recipient = raas_v2.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get("recipient")) if dictionary.get("recipient") else None
        sender = raas_v2.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get("sender")) if dictionary.get("sender") else None
        notes = dictionary.get("notes")

        # Return an object of this model
        return cls(account_identifier,
                   amount,
                   customer_identifier,
                   send_email,
                   utid,
                   campaign,
                   email_subject,
                   external_ref_id,
                   message,
                   recipient,
                   sender,
                   notes)


