from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits a PushFunds (OCT) request.

    :param data: **Required**. Instance of :func:`~pyvdp.visadirect.fundstransfer.PushFundsTransactionsModel`.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect import CardAcceptorModel, PointOfServiceDataModel
        from pyvdp.visadirect.fundstransfer import pushfundstransactions, PushFundsTransactionsModel
        
        posd_kwargs = {
            "motoECIIndicator": "0",
            "panEntryMode": "90",
            "posConditionCode": "00"            
        }
             
        address_kwargs = {
            "country": "USA",
            "county": "San Mateo",
            "state": "CA",
            "zipCode": "94404"        
        }
        
        card_acceptor_kwargs = {
            "address": CardAcceptorModel.CardAcceptorAddress(**address_kwargs),
            "idCode": "CA-IDCode-77765",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "TID-9999"        
        }
        
        data_kwargs = {
            "cardAcceptor": CardAcceptorModel(**ca_kwargs),
            "pointOfServiceData": PointOfServiceDataModel(**posd_kwargs),
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "amount": "124.05",
            "businessApplicationId": "AA",
            "recipientName": "rohan",
            "recipientPrimaryAccountNumber": "4957030420210462",
            "senderAccountNumber": "4957030420210454",
            "senderAddress": "901 Metro Center Blvd",
            "senderCity": "Foster City",
            "senderCountryCode": "124",
            "senderName": "Mohammed Qasim",
            "senderReference": "",
            "senderStateCode": "CA",
            "sourceOfFundsCode": "05",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015"                        
        }
        
        data = PushFundsTransactionsModel(**data_kwargs)
        result = pushfundstransactions.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='pushfundstransactions',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Fetches a status of previously submitted pushfundstransactions request.

    Returns a status of :func:`~pyvdp.visadirect.fundstransfer.PushFundsTransactionsModel` request by transaction 
    identifier, returned  with 202 response.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.fundstransfer import pushfundstransactions
        
        status_id = "1491819372_186_81_l73c003_VDP_ARM"
        result = pushfundstransactions.send(status_id)
        print(result)
    """
    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='pushfundstransactions',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
