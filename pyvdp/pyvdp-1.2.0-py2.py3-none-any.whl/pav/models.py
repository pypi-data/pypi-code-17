class CardValidationModel(object):
    """Visa Card Validation data object model.

    :param int systemsTraceAuditNumber: **Required**. Systems Trace Audit Number (STAN), 6-digits integer.
    :param str primaryAccountNumber: **Required**. Primary Account Number (PAN), 13-19 digits string.
    :param str cardExpiryDate: **Conditional**. Card expiration date, YYYY-MM. Required when cvv2 is present.
    :param AddressVerificationResults addressVerificationResults: **Conditional**. 
        Instance of :func:`~pyvdp.pav.CardValidationModel.AddressVerificationResults`.
    :param str cardCvv2Value: **Conditional**. Card CVV2 value. 3-4 characters string.
    :param int acquiringBin: **Optional**. Bank identification number under which a funds transfer is registered.
        6-11 digits integer.
    :param int acquirerCountryCode: **Optional**. 
        `ISO country code <https://developer.visa.com/request_response_codes#isoCodes>`_ for acquiring bank. 
        3 digits integer.
    :param CardAcceptorModel cardAcceptor: **Optional**. Instance of :func:`~pyvdp.visadirect.CardAcceptorModel`.

    **Request:**
        
    ..  code:: json

        {
            "addressVerificationResults": {
                "postalCode": "T4B 3G5",
                "street": "2881 Main Street Sw"
            },
            "cardAcceptor": {
                "address": {
                    "city": "fostr city",
                    "country": "PAKISTAN",
                    "county": "CA",
                    "state": "CA",
                    "zipCode": "94404"
                },
                "idCode": "111111",
                "name": "rohan",
                "terminalId": "123"
            },
            "cardCvv2Value": "672",
            "cardExpiryDate": "2018-06",
            "primaryAccountNumber": "4957030000313108",
            "retrievalReferenceNumber": "015221743720",
            "systemsTraceAuditNumber": "743720"
        }
        
    **Response:**
    
    ..  code:: json
    
        {
            "transactionIdentifier": 1234,
            "actionCode": "25",
            "responseCode": "5",
            "addressVerificationResults": "I",
            "cvv2ResultCode": "P"
        }    
    """
    ATTRS = [
        'systemsTraceAuditNumber',
        'primaryAccountNumber',
        'cardExpiryDate',
        'addressVerificationResults',
        'cardCvv2Value',
        'acquiringBin',
        'acquirerCountryCode',
        'cardAcceptor'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    class AddressVerificationResults(object):
        """AddressVerificationResults data object model.
        
        A subclass for Card Validation data object model.
        
        :param str street: **Conditional**. Street address for card holder. Required when cardCvv2Value
            is not present. 1-20 characters string.
        :param str postalCode: **Conditional**. Postal code for card holder address. Required when  cardCvv2Value is 
            not present. 1-20 characters string. 
        """
        ATTRS = [
            'street',
            'postalCode',
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
