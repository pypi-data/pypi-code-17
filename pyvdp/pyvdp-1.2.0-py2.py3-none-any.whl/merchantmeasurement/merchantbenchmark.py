from .dispatcher import VisaMerchantMeasurementDispatcher


def send(data):
    """Submits a MerchantBenchmark request.

    :param MerchantBenchmarkModel data: **Required**. 
        Instance of :func:`~pyvdp.merchantmeasurement.MerchantBenchmarkModel`.
    :return: A response from VDP.

    ..  code:: python
    
        from pyvdp.merchantmeasurement import merchantbenchmark, MerchantBenchmarkModel
            
        data_kwargs = {
            'merchantCategoryCodes': ['5812'],
            'merchantCategoryGroupsCodes': [''],
            'zipList': ['77027'],
            'msaList': [''],
            'countryList': [''],
            'monthList': ['201501'],
            'groupList': ['standard'],
                'cardPresentIndicator': '2'
        }
                    
        data_kwargs = {
            'requestData': MerchantBenchmarkModel.RequestData(**data_kwargs)
        }
            
        data = MerchantBenchmarkModel(**data_kwargs)
        result = merchantbenchmark.send(data)
        print(result)
    """
    c = VisaMerchantMeasurementDispatcher(resource='merchantmeasurement',
                                          api='',
                                          method='merchantbenchmark',
                                          http_verb='POST',
                                          data=data)
    return c.send()
