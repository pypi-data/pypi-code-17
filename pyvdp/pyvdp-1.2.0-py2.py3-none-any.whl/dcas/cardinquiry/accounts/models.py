class DebitCardInquiryModel(object):
    """Debit Card Inquiry data object model.
        
    :param str directDebitAccountNumber: **Required**. Direct debit account number. 6-22 characters string.
    :param str routingNumber: **Required**. Routing number. 6-12 characters string.
    :param CardholderName cardholderName: **Optional**. 
        Instance of :func:`~pyvdp.dcas.cardinquiry.accounts.DebitCardInquiryModel.CardholderName`
    
    **Request:**
        ..  code:: json
        
            {
                "directDebitAccountNumber": "0987654321",
                "routingNumber": "1234567890",
                "cardholderName": {
                    "firstName": "JACK",
                    "lastName": "DADE"
                }
            }
    
    **Response:**
        ..  code:: json
        
            {
                "resource": {
                    "debitCards": [
                        {
                            "primaryAccountNumber": "4031600000000010",
                            "sequenceOnCard": " ",
                            "expirationDate": {
                                "mm": 10,
                                "yy": 15
                            },
                            "activationStatus": "Y",
                            "cardStatus": " ",
                            "shouldCaptureCard": false,
                            "cardholderName": {
                                "firstName": "JACK",
                                "lastName": "DADE",
                                "middleName": " ",
                                "title": " ",
                                "suffix": " "
                            },
                            "cardholderAddress": {
                                "addressLine1": "8910 S RIDGELINE",
                                "addressLine2": " ",
                                "addressLine3": null,
                                "city": "DENVER",
                                "postalCode": "80166",
                                "region": "CO",
                                "country": null
                            }
                        },
                        { ... },
                        { ... },
                        { ... },
                    ]
                },
                "processingTimeInMs": 163,
                "receivedTimestamp": "11/18/2016 2:26:04 PM",
                "error": ""
            }            
    """
    ATTRS = [
        'directDebitAccountNumber',
        'routingNumber',
        'cardholderName'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    class CardholderName(object):
        """Cardholder name data object model.
        
        Part of :func:`~pyvdp.dcas.cardinquiry.accounts.DebitCardInquiryModel`.
        
        :param str firstName: **Optional**. Cardholder first name.
        :param str lastName: **Optional**. Cardholder last name.
        """
        ATTRS = [
            'firstName',
            'lastName'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
