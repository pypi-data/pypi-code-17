from pyvdp.globalatmlocator.dispatcher import VisaGlobalAtmLocatorDispatcher


def send(data):
    """Submits a Totals Inquiry request.

    :param TotalsInquiryModel data: **Required**. 
        Instance of :func:`~pyvdp.globalatmlocator.localatms.TotalsInquiryModel`.
    :return: A response from VDP.

    **Usage:**

    ..  code:: python
    
        from pyvdp.globalatmlocator.localatms import totalsinquiry, TotalsInquiryModel
    
        header_kwargs = {
            "applicationId": "VATMLOC",
            "correlationId": "909420141104053819418",
            "requestMessageId": "test12345678",
            "userBid": "10000108",
            "userId": "CDISIUserID"        
        }
        
        location_kwargs = {
            "placeName": "800 metro center , foster city,ca"        
        }
        
        range_kwargs = {
            "count": 99,
            "start": 0
        }
        
        sort_kwargs = {
            "direction": "desc",
            "primary": "city"        
        }
        
        filters = [
            {
                "filterName": "PLACE_NAME",
                "filterValue": "FORT FINANCIAL CREDIT UNION|ULTRON INC|U.S. BANK"
            },
            {
                "filterName": "OPER_HRS",
                "filterValue": "C"
            },
            {
                "filterName": "AIRPORT_CD",
                "filterValue": ""
            },
            {
                "filterName": "WHEELCHAIR",
                "filterValue": "N"
            },
            {
                "filterName": "BRAILLE_AUDIO",
                "filterValue": "N"
            },
            {
                "filterName": "BALANCE_INQUIRY",
                "filterValue": "N"
            },
            {
                "filterName": "CHIP_CAPABLE",
                "filterValue": "N"
            },
            {
                "filterName": "PIN_CHANGE",
                "filterValue": "N"
            },
            {
                "filterName": "RESTRICTED",
                "filterValue": "N"
            },
            {
                "filterName": "PLUS_ALLIANCE_NO_SURCHARGE_FEE",
                "filterValue": "N"
            },
            {
                "filterName": "ACCEPTS_PLUS_SHARED_DEPOSIT",
                "filterValue": "N"
            },
            {
                "filterName": "V_PAY_CAPABLE",
                "filterValue": "N"
            },
            {
                "filterName": "READY_LINK",
                "filterValue": "N"
            }
        ]
        
        options_kwargs = {
            "findFilters": filters,
            "operationName": "or",
            "range": TotalsInquiryModel.RequestData.Options.Range(**range_kwargs),
            "sort": TotalsInquiryModel.RequestData.Options.Sort(**sort_kwargs),
            "useFirstAmbiguous": True
        }
        
        request_kwargs = {
            "culture": "en-US",
            "distance": "20",
            "distanceUnit": "mi",
            "location": TotalsInquiryModel.RequestData.Location(**location_kwargs),
            "metaDataOptions": 0,
            "options": TotalsInquiryModel.RequestData.Options(**options_kwargs)
        }
        
        data_kwargs = {
            "wsRequestHeaderV2": TotalsInquiryModel.WsRequestHeaderV2(**header_kwargs),
            "requestData": TotalsInquiryModel.RequestData(**request_kwargs)
        }
        
        data = TotalsInquiryModel(**data_kwargs)
        result = totalsinquiry.send(data)
        print(result)
    """
    c = VisaGlobalAtmLocatorDispatcher(resource='globalatmlocator',
                                       api='',
                                       method='localatms/totalsinquiry',
                                       http_verb='POST',
                                       data=data)
    return c.send()
