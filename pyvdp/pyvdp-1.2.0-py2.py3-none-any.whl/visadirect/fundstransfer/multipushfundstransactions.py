from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits a MultiPushFundsTransactions (OCT) request.

    :param data: **Required**. Instance of  :func:`~pyvdp.visadirect.fundstransfer.MultiPushFundsTransactionsModel`.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect import CardAcceptorModel, PointOfServiceDataModel
        from pyvdp.visadirect.fundstransfer import multipushfundstransactions, MultiPushFundsTransactionsModel
        
        address_kwargs = {
            "country": "USA",
            "county": "00",
            "state": "CA",
            "zipCode": "94454"        
        }
        
        card_acceptor_kwargs = {
            "address": CardAcceptorModel.Address(**address_kwargs),
            "idCode": "5678",
            "name": "Mr Smith",
            "terminalId": "1234"            
        }
        
        request = {
            "amount": 100.00,
            "feeProgramIndicator": "123",
            "recipientName": "Akhila",
            "recipientPrimaryAccountNumber": "4957030420210454",
            "retrievalReferenceNumber": "401010101011",
            "senderAccountNumber": "4005520000011126",
            "senderAddress": "My Address",
            "senderCity": "My City",
            "senderCountryCode": "USA",
            "senderName": "Mr Name",
            "senderReference": "",
            "senderStateCode": "CA",
            "sourceOfFundsCode": "01",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "234234234234234",
            "cardAcceptor": CardAcceptorModel(**card_acceptor_kwargs)
        }
        
        data_kwargs = {
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "businessApplicationId": "AA",
            "localTransactionDateTime": "2017-04-21T03:25:21",
            "merchantCategoryCode": "6012",
            "request": [
                request
            ]
        }
        
        data = PushFundsTransactionsModel(**data_kwargs)
        result = multipushfundstransactions.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='multipushfundstransactions',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Fetches a status of previously submitted PushFunds request.

    Returns a status of :func:`~pyvdp.visadirect.fundstransfer.MultiPushFundsTransactionsModel` request by transaction 
    identifier, returned with 202 response.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.visadirect.fundstransfer import multipushfundstransactions
        
        status_id = "1491819372_186_81_l73c003_VDP_ARM"
        result = pushfundstransactions.send(status_id)
        print(result)
    """
    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='multipushfundstransactions',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
