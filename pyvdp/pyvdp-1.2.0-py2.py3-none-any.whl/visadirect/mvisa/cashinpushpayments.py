from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits VisaDirect mVISA CashinPushPayments request.

    :param CashinPushPaymentsModel data: **Required**. 
        Instance of :func:`~pyvdp.visadirect.mvisa.CashinPushPaymentsModel`.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python

        from pyvdp.visadirect.mvisa import cashinpushpayments, CashinPushPaymentsModel    
        from pyvdp.visadirect import CardAcceptorModel

        address_kwargs = {
            "city": "KOLKATA",
            "country": "IND"
        }
        
        card_acceptor_kwargs = {
            "address": CardAcceptorModel.CardAcceptorAddress(**address_kwargs),
            "idCode": "CA-IDCode-77765",
            "name": "Visa Inc. USA-Foster City"            
        }
        
        data_kwargs = {
            "acquirerCountryCode": "643",
            "acquiringBin": "400171",
            "amount": "124.05",
            "businessApplicationId": "CI",            
            "cardAcceptor": CardAcceptorModel(**card_acceptor_kwargs),
            "merchantCategoryCode": "4829",
            "recipientPrimaryAccountNumber": "4123640062698797",
            "senderAccountNumber": "4541237895236",
            "senderName": "Mohammed Qasim",
            "senderReference": "1234",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015"                                        
        }
        
        data = CashinPushPaymentsModel(**data_kwargs)
        result = cashinpushpayments.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='mvisa',
                             method='cashinpushpayments',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Sends VisaDirect mVISA CashinPushPayments request.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.mvisa import cashinpushpayments
        
        status_id = '1491819372_186_81_l73c003_VDP_ARM'
        result = cashinpushpayments.get(status_id)
        print(result)
    """
    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='mvisa', method='cashinpushpayments',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
