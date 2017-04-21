from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits a ReverseFundsTransactions request.

    :param data: **Required**. Instance of :func:`~pyvdp.visadirect.fundstransfer.ReverseFundsTransactionsModel`
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect import (CardAcceptorModel, 
                                      OriginalDataElementsModel, 
                                      PointOfServiceCapabilityModel, 
                                      PointOfServiceDataModel)
                                      
        from pyvdp.visadirect.fundstransfer import reversefundstransactions, ReverseFundsTransactionsModel
        
        ode_kwargs = {
            "acquiringBin": "408999",
            "approvalCode": "20304B",
            "systemsTraceAuditNumber": "897825",
            "transmissionDateTime": "2017-03-17T09:02:32"        
        }
        
        posc_kwargs = {
            "posTerminalEntryCapability": "2",
            "posTerminalType": "4"        
        }
        
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
            "idCode": "VMT200911026070",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "365539"                    
        }
        
        data_kwargs = {
            "cardAcceptor": CardAcceptorModel(**card_acceptor_kwargs),
            "originalDataElements": OriginalDataElementsModel(**ode_kwargs),
            "pointOfServiceCapability": PointOfServiceCapabilityModel(**posc_kwargs),
            "pointOfServiceData": PointOfServiceDataModel(**posd_kwargs),
            "senderCardExpiryDate": "2015-10",
            "senderCurrencyCode": "USD",
            "senderPrimaryAccountNumber": "4895100000055127",
            "transactionIdentifier": "381228649430011",
            "acquirerCountryCode": "608",
            "acquiringBin": "408999",
            "amount": "24.01",                        
        }
        
        data = ReverseFundsTransactionsModel(**data_kwargs)
        result = reversefundstransactions.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='reversefundstransactions',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Fetches a status of previously submitted ReverseFundsTransactions request.

    Returns a status of :func:`~pyvdp.visadirect.fundstransfer.ReverseFundsTransactionsModel` request by transaction 
    identifier, returned with 202 response.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.fundstransfer import reversefundstransactions
        
        status_id = '1491819372_186_81_l73c003_VDP_ARM'
        
        result = reversefunds.get(status_id)
        print(result)
    """
    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='reversefundstransactions',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
