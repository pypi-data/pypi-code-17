from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits VisaDirect mVISA CashoutPushPayments request.

    :param CashoutPushPaymentsModel data: **Required**. 
        Instance of :func:`~pyvdp.visadirect.mvisa.CashoutPushPaymentsModel`.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.mvisa import cashoutpushpayments, CashoutPushPaymentsModel
        from pyvdp.visadirect import CardAcceptorModel
        
        address_kwargs = {
            "city": "mVisa cashout",
            "country": "IND"            
        }
        
        card_acceptor_kwargs = {
            "address": CardAcceptorModel.CardAcceptorAddress(**address_kwargs),
            "idCode": "CA-IDCode-77765",
            "name": "mVisa cashout"        
        }
        
        data_kwargs = {
            "acquirerCountryCode": "643",
            "acquiringBin": "400171",
            "amount": "124.05",
            "businessApplicationId": "CO",
            "address": CardAcceptorModel(**card_acceptor_kwargs),
            "merchantCategoryCode": "6012",
            "recipientPrimaryAccountNumber": "4123640062698797",
            "senderAccountNumber": "456789123456",
            "senderName": "Mohammed Qasim",
            "senderReference": "REFNUM123",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015"            
        }
        
        data = CashoutPushPaymentsModel(**data_kwargs)
        result = cashoutpushpayments.send(data)
        print(result)
        
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='mvisa',
                             method='cashoutpushpayments',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Sends VisaDirect mVISA CashoutPushPayments request.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.mvisa import cashoutpushpayments
        
        status_id = '1491819372_186_81_l73c003_VDP_ARM'
        result = cashoutpushpayments.get(status_id)
        print(result)
    """
    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='mvisa',
                             method='cashoutpushpayments',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
