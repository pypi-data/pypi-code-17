from .dispatcher import VisaForexRatesDispatcher


def send(data):
    """Submits a Forex Rates Exchange request.

    :param ForeignExchangeRatesModel data: **Required**. 
        Instance of :func:`~pyvdp.forexrates.ForeignExchangeRatesModel`.
    :return: Response from VDP.
    
    **Usage:**
    
    ..  code-block:: python
    
            from pyvdp.forexrates import foreignexchangerates, ForeignExchangeRatesModel
    
            data_kwargs = {
                'destination_cur_code': '840',
                'source_amount': 100.00,
                'source_cur_code': 643
            }
    
            data = ForeignExchangeRatesModel(**data_kwargs)
            result = foreignexchangerates.send(data)
            print(result)
    """
    c = VisaForexRatesDispatcher(resource='forexrates',
                                 api='',
                                 method='foreignexchangerates',
                                 http_verb='POST',
                                 data=data)
    return c.send()
