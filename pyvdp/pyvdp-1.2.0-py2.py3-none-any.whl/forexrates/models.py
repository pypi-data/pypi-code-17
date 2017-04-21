class ForeignExchangeRatesModel(object):
    """Foreign Exchange Rates data object model.
        
    :param str destinationCurrencyCode: **Required**. 
        Source currency `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_.
        3 characters string.
    :param str sourceCurrencyCode: **Required**. 
        Destination currency `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_.
        3 characters string.
    :param float sourceAmount: **Required**. Amount of source currency to exchange. 3 digits, 2 fractions float. 
    :param str markUpRate: **Optional**. Exchange markup rate if client wants to apply a certain markup rate.
        0-6 characters string. E.g. 0.07 equals to 0.07% markup rate.
    :param int systemsTraceAuditNumber: **Optional**. Systems Trace Audit Number. 6 digits integer.
    :param int acquiringBin: **Optional**. Acquiring BIN for funds transfer operations. 6-11 digits integer.
    :param str acquirerCountryCode: **Optional**. 
        Acquirer `ISO country code <https://developer.visa.com/request_response_codes#isoCodes>`_  for BIN provided. 
        3 characters numeric string.
    :param CardAcceptorModel cardAcceptor: **Optional**. Instance of :func:`~pyvdp.visadirect.CardAcceptorModel`
    
    **Request:**
    
    ..  code:: json
    
        {
            "cardAcceptor": {
                "address": {
                    "city": "Foster City",
                    "country": "RU",
                    "county": "San Mateo",
                    "state": "CA",
                    "zipCode": "94404"
                },
                "idCode": "ABCD1234ABCD123",
                "name": "ABCD",
                "terminalId": "ABCD1234"
            },
            "destinationCurrencyCode": "840",
            "markUpRate": "1",
            "retrievalReferenceNumber": "201010101031",
            "sourceAmount": "100",
            "sourceCurrencyCode": "643",
            "systemsTraceAuditNumber": "350421"
        }
                
    **Response:**
    
    ..  code:: json
    
        {
            "conversionRate": "0.0318",
            "destinationAmount": "3.14",
            "markUpRateApplied": "1.0",
            "originalDestnAmtBeforeMarkUp": "3.18"
        }        
    """
    ATTRS = [
        'destinationCurrencyCode',
        'sourceCurrencyCode',
        'sourceAmount',
        'markUpRate',
        'systemsTraceAuditNumber',
        'acquiringBin',
        'acquirerCountryCode',
        'cardAcceptor'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)
