from pyvdp.visadirect import VisaDirectTransactionModel


class CashinPushPaymentsModel(VisaDirectTransactionModel):
    """VisaDirect mVISA CashinPushPayments data object model.

    :param int systemsTraceAuditNumber: **Required**. Systems trace audit number. 6 digits integer.
    :param str recipientPrimaryAccountNumber: **Required**. Recipient primary account number (PAN). 
        13-19 characters string.
    :param float amount: **Required**. Transaction amount. 12 digits, 3 fractions.
    :param int merchantCategoryCode: **Optional**. Merchant category code, populated by Originator. 
        4 digits integer. **6012** for mVISA.
    :param int acquiringBin: **Required**. Business identification number. 6-11 digits integer.
    :param int acquirerCountryCode: **Required**. 
        Country `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_  of originator BIN. 
        3 digits integer.
    :param CardAcceptorModel cardAcceptor: **Required**. Instance of :func:`~pyvdp.visadirect.CardAcceptorModel` data 
        object.
    :param str transactionCurrencyCode: **Required**. 
        Transaction currency `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_.
        3 characters string.
    :param str businessApplicationId: **Required**. Business application identifier. **CI** for cash-in operations.
        See `BAI codes <https://developer.visa.com/request_response_codes#businessApplicationId>`_ for details.
    :param str senderReference: **Optional**. Unique agent reference. Max 16 characters string.
    :param str senderAccountNumber: **Optional**. Sender account number.
    :param str senderName: **Required**. Agent name. Max 30 characters string.
    
    **Request:**
    
    ..  code:: json

        {
            "acquirerCountryCode": "643",
            "acquiringBin": "400171",
            "amount": "124.05",
            "businessApplicationId": "CI",
            "cardAcceptor": {
                "address": {
                    "city": "Bangalore",
                    "country": "IND"
                },
                "idCode": "ID-Code123",
                "name": "Card Accpector ABC"
            },
            "localTransactionDateTime": "2017-04-21T04:10:22",
            "merchantCategoryCode": "4829",
            "recipientPrimaryAccountNumber": "4123640062698797",
            "retrievalReferenceNumber": "430000367618",
            "senderAccountNumber": "4541237895236",
            "senderName": "Mohammed Qasim",
            "senderReference": "1234",
            "systemsTraceAuditNumber": "313042",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015"
        }
        
    **Response:**
    
    ..  code:: json
    
        {
            "transactionIdentifier": 23423432,
            "actionCode": "00",
            "approvalCode": "21324K",
            "responseCode": "5",
            "transmissionDateTime": "2017-04-21T04:10:44.000Z",
            "retrievalReferenceNumber": "430000367618"
        }    
    """
    ATTRS = [
        'recipientPrimaryAccountNumber',
        'amount',
        'merchantCategoryCode',
        'acquiringBin',
        'acquirerCountryCode',
        'cardAcceptor',
        'transactionCurrencyCode',
        'businessApplicationId',
        'senderReference',
        'senderAccountNumber',
        'senderName'
    ]

    def __init__(self, **kwargs):
        super(CashinPushPaymentsModel, self).__init__(**kwargs)
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)


class CashoutPushPaymentsModel(VisaDirectTransactionModel):
    """VisaDirect mVISA CashoutPushPayments data object model.

    :param int systemsTraceAuditNumber: **Required**. Systems trace audit number. 6 digits integer.
    :param str recipientPrimaryAccountNumber: **Required**. Recipient primary account number (PAN). 
        13-19 characters string.
    :param float amount: **Required**. Transaction amount. 12 digits, 3 fractions.
    :param int merchantCategoryCode: **Optional**. Merchant category code, populated by Originator. 
        4 digits integer. **6012** for mVISA.
    :param int acquiringBin: **Required**. Business identification number. 6-11 digits integer.
    :param int acquirerCountryCode: **Required**. 
        Country `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_ of originator BIN. 
        3 digits integer.
    :param CardAcceptorModel cardAcceptor: **Required**. 
        Instance of :func:`~pyvdp.visadirect.CardAcceptorModel` data object.
    :param str transactionCurrencyCode: **Required**. 
        Transaction currency `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_.
        3 characters string.
    :param str businessApplicationId: **Required**. Business application identifier. **CO** for cash-out operations.
        See `BAI codes <https://developer.visa.com/request_response_codes#businessApplicationId>`_ for details.
    :param str senderReference: **Optional**. Unique agent reference. Max 16 characters string.
    :param str senderAccountNumber: **Optional**. Sender account number.
    :param str senderName: **Required**. Agent name. Max 30 characters string.

    **Request:**
    
    ..  code:: json
    
        {
            "acquirerCountryCode": "643",
            "acquiringBin": "400171",
            "amount": "124.05",
            "businessApplicationId": "CO",
            "cardAcceptor": {
                "address": {
                    "city": "mVisa cashout",
                    "country": "IND"
                },
                "idCode": "CA-IDCode-77765",
                "name": "mVisa cashout"
            },
            "localTransactionDateTime": "2017-04-21T04:12:21",
            "merchantCategoryCode": "6012",
            "recipientPrimaryAccountNumber": "4123640062698797",
            "retrievalReferenceNumber": "412123412878",
            "senderAccountNumber": "456789123456",
            "senderName": "Mohammed Qasim",
            "senderReference": "REFNUM123",
            "systemsTraceAuditNumber": "567889",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015"
        }
        
    **Response:**
    
    ..  code:: json
    
        {
            "transactionIdentifier": 23423432,
            "actionCode": "00",
            "approvalCode": "21324K",
            "responseCode": "5",
            "transmissionDateTime": "2017-04-21T04:12:26.000Z",
            "retrievalReferenceNumber": "412123412878",
            "cardAcceptor": {
                "name": "mVisa Merchant",
                "address": {
                    "city": "mVisa City",
                    "country": "IN"
                }
            }
        }    
    """
    ATTRS = [
        'recipientPrimaryAccountNumber',
        'amount',
        'merchantCategoryCode',
        'acquiringBin',
        'acquirerCountryCode',
        'transactionCurrencyCode',
        'cardAcceptor',
        'businessApplicationId',
        'senderAccountNumber',
        'senderReference',
        'senderName'
    ]

    def __init__(self, **kwargs):
        super(CashoutPushPaymentsModel, self).__init__(**kwargs)
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)


class MerchantPushPaymentsModel(VisaDirectTransactionModel):
    """VisaDirect mVISA MerchantPushPayments data object model.

    :param int systemsTraceAuditNumber: **Required**. Systems trace audit number. 6 digits integer.
    :param str recipientPrimaryAccountNumber: **Required**. Recipient primary account number (PAN). 
        13-19 characters string.
    :param float amount: **Required**. Transaction amount. 12 digits, 3 fractions.
    :param int merchantCategoryCode: **Optional**. Merchant category code, populated by Originator. 
        4 digits integer. **6012** for mVISA.
    :param int acquiringBin: **Required**. Business identification number. 6-11 digits integer.
    :param int acquirerCountryCode: **Required**. 
        Country `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_  of originator BIN. 
        3 digits integer.
    :param float transactionFeeAmount: **Required**. Convenience fee amount. 8 digits, 3 fractions. 
    :param CardAcceptorModel cardAcceptor: **Required**. 
        Instance of :func:`~pyvdp.visadirect.CardAcceptorModel` data object.
    :param str transactionCurrencyCode: **Required**. 
        Transaction currency `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_. 3 characters 
        string.
    :param PurchaseIdentifierModel purchaseIdentifier: **Required**. 
        Instance of :func:`~pyvdp.visadirect.mvisa.PurchaseIdentifier`.
    :param str recipientName: Recipient name.
    :param str secondaryId: **Conditional**. Second field with additional transaction data. Max 28 characters string. 
    :param str businessApplicationId: **Required**. Business application identifier. **MP** for merchant payments 
        operations. See `BAI codes <https://developer.visa.com/request_response_codes#businessApplicationId>`_ for 
        details.
    :param str senderReference: **Optional**. Unique agent reference. Max 16 characters string.
    :param str senderAccountNumber: **Required**. Sender account number. Max 34 characters string.
    :param str senderName: **Required**. Agent name. Max 30 characters string.

    **Request:**
    
    ..  code:: json
    
        {
            "acquirerCountryCode": "356",
            "acquiringBin": "408972",
            "amount": "124.05",
            "businessApplicationId": "MP",
            "cardAcceptor": {
                "address": {
                    "city": "KOLKATA",
                    "country": "IND"
                },
                "idCode": "CA-IDCode-77765",
                "name": "Visa Inc. USA-Foster City"
            },
            "feeProgramIndicator": "123",
            "localTransactionDateTime": "2017-04-21T04:13:43",
            "purchaseIdentifier": {
                "referenceNumber": "REF_123456789123456789123",
                "type": "1"
            },
            "recipientName": "Jasper",
            "recipientPrimaryAccountNumber": "4123640062698797",
            "retrievalReferenceNumber": "412770451035",
            "secondaryId": "123TEST",
            "senderAccountNumber": "4027290077881587",
            "senderName": "Jasper",
            "senderReference": "",
            "systemsTraceAuditNumber": "451035",
            "transactionCurrencyCode": "INR",
            "transactionIdentifier": "381228649430015"
        }
         
    **Response:**
    
    ..  code:: json
    
        {
            "transactionIdentifier": 23423432,
            "actionCode": "00",
            "approvalCode": "21324K",
            "responseCode": "5",
            "transmissionDateTime": "2017-04-21T04:13:47.000Z",
            "retrievalReferenceNumber": "412770451035",
            "purchaseIdentifier": {
                "type": "1",
                "referenceNumber": "REF_123456789123456789123"
            },
            "feeProgramIndicator": "123",
            "merchantCategoryCode": 5812,
            "cardAcceptor": {
                "name": "mVisa Merchant",
                "terminalId": "MER-ID00",
                "idCode": "MvisaMerchant-1",
                "address": {
                    "city": "mVisa City",
                    "country": "IN"
                }
            },
            "merchantVerificationValue": "0A45AF98FC"
        }    
    """
    ATTRS = [
        'recipientPrimaryAccountNumber',
        'amount',
        'merchantCategoryCode',
        'acquiringBin',
        'acquirerCountryCode',
        'transactionFeeAmount',
        'cardAcceptor',
        'transactionCurrencyCode',
        'purchaseIdentifier',
        'secondaryId',
        'businessApplicationId',
        'recipientName',
        'senderReference',
        'senderAccountNumber',
        'senderName',
    ]

    def __init__(self, **kwargs):
        super(MerchantPushPaymentsModel, self).__init__(**kwargs)
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)


class PurchaseIdentifierModel(object):
    """VisaDirect mVISA PurchaseIdentifierModel data object model.

    Used as a part of :func:`~pyvdp.visadirect.mvisa.MerchantPushPaymentsModel`.

    :param str type: **Required**. Primary ID as defined by mVISA. 1 character string.
    :param str referenceNumber: **Required**. Key data element for matching a message to others within a given
        transaction set. Value will be the same as what has been provided in the request. Max 13 characters string.
    """
    ATTRS = [
        'type',
        'referenceNumber',
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)
