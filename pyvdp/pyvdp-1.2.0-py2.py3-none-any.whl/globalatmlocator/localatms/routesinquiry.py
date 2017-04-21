from pyvdp.globalatmlocator.dispatcher import VisaGlobalAtmLocatorDispatcher


def send(data):
    """Submits a Routes Inquiry request.

    :param RoutesInquiryModel data: **Required**. 
        Instance of :func:`~pyvdp.globalatmlocator.localatms.RoutesInquiryModel`.
    :return: Response from VDP

    **Usage:**
    
    ..  code:: python
    
        from pyvdp.globalatmlocator.localatms import routesinquiry, RoutesInquiryModel
        
        header_kwargs = {
            "applicationId": "GEOCODE",
            "correlationId": "909420141104053819418",
            "requestMessageId": "ICE01-001",
            "userBid": "10000108",
            "userId": "CDISIUserID"        
        }
        
        geom1_kwargs = {
            "x": -122.4079,
            "y": 37.78356
        }
        
        geom2_kwargs = {
            "x": -122.404,
            "y": 37.782        
        }
        
        features = [
            {
                "geometry": RoutesInquiryModel.RequestData.Geometry(**geom1_kwargs),
            },
            {
                "geometry": RoutesInquiryModel.RequestData.Geometry(**geom2_kwargs),
            }
        ]
        
        travel_mode_kwargs = {
            "type": "WALKINGTIME"
        }
        
        request_kwargs = {
            "doNotLocateOnRestrictedElements": True,
            "features": features,
            "travelMode": RoutesInquiryModel.RequestData.TravelMode(**travel_mode_kwargs),
            "type": "features"
        }
        
        data_kwargs = {
            "wsRequestHeaderV2": RoutesInquiryModel.WsRequestHeaderV2(**header_kwargs),
            "requestData": RoutesInquiryModel.RequestData(**request_kwargs)
        }
        
        data = RoutesInquiryModel(**data_kwargs)
        result = routesinquiry.send(data)
        print(result) 
    """
    c = VisaGlobalAtmLocatorDispatcher(resource='globalatmlocator',
                                       api='',
                                       method='localatms/routesinquiry',
                                       http_verb='POST',
                                       data=data)
    return c.send()
