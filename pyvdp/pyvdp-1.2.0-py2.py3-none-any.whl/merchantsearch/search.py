from pyvdp.merchantsearch import VisaMerchantSearchDispatcher


def send(data):
    """Submits a Merchant Search request.

    :param MerchantSearch data: **Required**. Instance of :func:`~pyvdp.merchantsearch.MerchantSearchData`.
    :return: A response from VDP.
    
    **Usage:**
    
    ..  code-block:: python
    
        from pyvdp.merchantsearch import search, SearchModel
        
        search_attrs = {
            "merchantName": "cmu edctn materials cntr",
            "merchantStreetAddress": "802 industrial dr",
            "merchantCity": "Mount Pleasant",
            "merchantState": "MI",
            "merchantPostalCode": "48858",
            "merchantCountryCode": "840",
            "merchantPhoneNumber": "19897747123",
            "merchantUrl": "http://www.emc.cmich.edu",
            "businessRegistrationId": "386004447",
            "acquirerCardAcceptorId": "424295031886",
            "acquiringBin": "476197"
        }
        
        search_options = {
            "maxRecords": "5",
            "matchIndicators": "true",
            "matchScore": "true",
            "proximity": [
                "merchantName"
            ],
            "wildCard": [
                "merchantName"
            ]
        }
        
        data_kwargs = {
            'searchAttrList': SearchModel.MerchantSearchAttrList(**search_attrs),
            'searchOptions': SearchModel.MerchantSearchOptions(**search_options),        
        }
        
        data = SearchModel(**data_kwargs)
        result = search.send(data)
        print(result)
    """
    c = VisaMerchantSearchDispatcher(resource='merchantsearch',
                                     api='',
                                     method='search',
                                     http_verb='POST',
                                     data=data)
    return c.send()
