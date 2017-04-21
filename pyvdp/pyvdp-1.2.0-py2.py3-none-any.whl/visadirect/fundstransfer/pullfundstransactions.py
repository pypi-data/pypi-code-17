from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits a PullFundsTransactions (AFT) request.

    :param data: **Required**. Instance of :func:`~pyvdp.visadirect.fundstransfer.PullFundsTransactionsModel`.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect import CardAcceptorModel
        from pyvdp.visadirect.fundstransfer import pullfundstransactions, PullFundsTransactionsModel
        
        address_kwargs = {
            "country": "USA",
            "county": "San Mateo",
            "state": "CA",
            "zipCode": "94404"            
        }
        
        card_acceptor_kwargs = {
            "address": CardAcceptorModel.CardAcceptorAddress(**address_kwargs),
            "idCode": "ABCD1234ABCD123",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "ABCD1234"            
        }
        
        data_kwargs = {
            "cardAcceptor": CardAcceptorModel(**ca_kwargs),
            "acquirerCountryCode": 840,
            "acquiringBin": 408999,
            "amount": 124.02,
            "businessApplicationId": "AA",
            "cavv": "0700100038238906000013405823891061668252",
            "foreignExchangeFeeTransaction": "11.99",
            "localTransactionDateTime": "2017-03-17T08:20:42",
            "senderCardExpiryDate": "2015-10",
            "senderCurrencyCode": "USD",
            "senderPrimaryAccountNumber": "4895142232120006",
            "surcharge": "11.99",                            
        }
        
        data = PullFundsTransactionsModel(**data_kwargs)
        result = pullfundstransactions.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='pullfundstransactions',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Fetches a status of previously submitted :func:`~pyvdp.visadirect.fundstransfer.pullfundstransactions` request.
    
    Returns a status of :func:`~pyvdp.visadirect.fundstransfer.PullFundsTransactionsModel` request by 
    transaction identifier,  returned with  202 response.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
        
        from pyvdp.visadirect.fundstransfer import pullfundstransactions
        
        status_id = '1491819372_186_81_l73c003_VDP_ARM'
        result = pullfunds.get(status_id)
        print(result)
    """

    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='pullfundstransactions',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
