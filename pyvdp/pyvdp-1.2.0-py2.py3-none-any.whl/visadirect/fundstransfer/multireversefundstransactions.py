from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits a MultiReverseFundsTransactions request.

    :param data: **Required**. Instance of :func:`~pyvdp.visadirect.fundstransfer.MultiReverseFundsTransactionsModel`
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect import (CardAcceptorModel, 
                                      OriginalDataElementsModel)
                                      
        from pyvdp.visadirect.fundstransfer import multireversefundstransactions, MultiReverseFundsTransactionsModel
        
        address_kwargs = {
            "country": "USA",
            "county": "00",
            "state": "CA",
            "zipCode": "94454"        
        }
        
        card_acceptor_kwargs = {
            "amount": "100.00",
            "idCode": "5678",
            "name": "Mr Smith",
            "terminalId": "1234",
            "address": CardAcceptorModel.Address(**address_kwargs)
        }
        
        ode_kwargs = {
            "acquiringBin": "408999",
            "approvalCode": "1ABCDE",
            "systemsTraceAuditNumber": "228112",
            "transmissionDateTime": "2017-04-21T03:56:17",                    
        }
        
        request = {
            "amount": "100.00",
            "cardAcceptor": CardAcceptorModel(**card_acceptor_kwargs),
            "originalDataElements": OriginalDataElementsModel(**ode_kwargs),
            "retrievalReferenceNumber": "401010101011",
            "senderCardExpiryDate": "2020-12",
            "senderCurrencyCode": "USD",
            "senderPrimaryAccountNumber": "4485810000000131",
            "systemsTraceAuditNumber": "101011",
            "transactionIdentifier": "101010101010"            
        }
        
        data_kwargs = {
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "request": [
                request
            ]            
        }
        
        data = MultiReverseFundsTransactionsModel(**data_kwargs)
        result = multireversefundstransactions.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='multireversefundstransactions',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Fetches a status of previously submitted MultiReverseFundsTransactions request.

    Returns a status of :func:`~pyvdp.visadirect.fundstransfer.MultiReverseFundsTransactionsModel` request by 
    transaction identifier, returned with 202 response.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.fundstransfer import multireversefundstransactions
        
        status_id = '1491819372_186_81_l73c003_VDP_ARM'
        
        result = multireversefundstransactions.get(status_id)
        print(result)
    """
    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='multireversefundstransactions',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
