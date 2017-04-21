from pyvdp.visadirect import VisaDirectDispatcher


def send(data):
    """Submits a MultiPullFundsTransactions (AFT) request.

    :param data: **Required**. 
        Instance of  :func:`~pyvdp.visadirect.fundstransfer.MultiPullFundsTransactionsModel`.
    :return: Dictionary with VDP API response.

    **Usage:**

    ..  code:: python

        from pyvdp.visadirect import CardAcceptorModel
        from pyvdp.visadirect.fundstransfer import multipullfundstransactions, MultiPullFundsTransactionsModel

        address_kwargs = {
            "country": "USA",
            "county": "San Mateo",
            "state": "CA",
            "zipCode": "94404"            
        }

        card_acceptor_kwargs = {
            "address": CardAcceptorModel.CardAcceptorAddress(**ca_address_kwargs),
            "idCode": "ABCD1234ABCD123",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "ABCD1234"            
        }

        request = {
            "amount": 124.02,
            "cardAcceptor": CardAcceptorModel(**card_acceptor_kwargs),
            "cavv": "0700020718799100000002980179911000000000",
            "localTransactionDateTime": "2017-04-20T05:16:05",
            "retrievalReferenceNumber": "401010101011",
            "senderCardExpiryDate": "2020-12",
            "senderCurrencyCode": "USD",
            "senderPrimaryAccountNumber": "4895140000066666",
            "systemsTraceAuditNumber": "101011"
        }
        
        data_kwargs = {
            "acquirerCountryCode": "608",
            "acquiringBin": "408999",
            "businessApplicationId": "AA",
            "localTransactionDateTime": "2017-04-20T05:16:05",
            "merchantCategoryCode": "6012",
            "request": [
                request
            ]
        }

        data = MultiPullFundsTransactionsModel(**data_kwargs)
        result = multipullfundstransactions.send(data)
        print(result)
    """
    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='multipullfundstransactions',
                             http_verb='POST',
                             data=data)
    return c.send()


def get(status_id):
    """Fetches a status of previously submitted :func:`~pyvdp.visadirect.fundstransfer.multipullfundstransactions`
     request.

    Returns a status of :func:`~pyvdp.visadirect.fundstransfer.MultiPullFundsTransactionsModel` request by 
    transaction identifier,  returned with  202 response.

    :param str status_id: **Required**. Transaction status identifier.
    :return: Dictionary with VDP API response.

    **Usage:**

    ..  code:: python

        from pyvdp.visadirect.fundstransfer import multipullfundstransactions

        status_id = '1491819372_186_81_l73c003_VDP_ARM'
        result = multipullfundstransactions.get(status_id)
        print(result)
    """

    query_string = '/' + status_id

    c = VisaDirectDispatcher(resource='visadirect',
                             api='fundstransfer',
                             method='multipullfundstransactions',
                             http_verb='GET',
                             query_string=query_string)
    return c.send()
