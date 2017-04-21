from .dispatcher import VisaMerchantLocatorDispatcher


def send(data):
    """Submits a MerchantLocator request.

    :param LocatorModel data: **Required**. 
        Instance of :func:`~pyvdp.merchantlocator.LocatorModel`.
    :return: A response from VDP.
    
    **Usage:**
    
    ..  code:: python
    
            from pyvdp.merchantlocator import locator, LocatorModel
            
            search_attrs_kwargs = {
                "merchantName": "Starbucks",
                "merchantCountryCode": "840",
                "latitude": "37.363922",
                "longitude": "-121.929163",
                "distance": "2",
                "distanceUnit": "M"            
            }
            
            search_options_kwargs = {
                "maxRecords": "5",
                "matchIndicators": "true",
                "matchScore": "true"            
            }
            
            data_kwargs = {
                "searchAttrList": LocatorModel.SearchAttrList(**search_attrs_kwargs),
                "searchOptions": LocatorModel.SearchOptions(**search_options_kwargs),
                "responseAttrList": ["GNLOCATOR"]
            }
            
            data = LocatorModel(**data_kwargs)            
            result = locator.send(data)
            print(result)
    """
    c = VisaMerchantLocatorDispatcher(resource='merchantlocator',
                                      api='',
                                      method='locator',
                                      http_verb='POST',
                                      data=data)
    return c.send()
