from pyvdp.mlc.dispatcher import VisaMobileLocationConfirmationDispatcher


def send(data):
    """Submits MLC Location Update request.
    
    :param pyvdp.mlc.locationupdate.LocationsModel data: **Required**.  Instance of MLC Location Update model.
    :return: response from VDP.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.mlc.locationupdate import locations, LocationsModel
        
        geo_kwargs = {
            "latitude": "37.55862902",
            "longitude": "-122.2773385"        
        }
        
        header_kwargs = {
            "messageId": "2d099794-e69a-4acb-9485-5a643d231f51"        
        }
        
        data_kwargs = {
            "header": LocationsModel.Header(**header_kwargs),
            "geoLocationCoordinate": LocationsModel.GeoLocationCoordinate(**geo_kwargs),
            "accuracy": "5000",
            "cloudNotificationKey": "03e3ae03-a627-4241-bad6-58f811c18e46",
            "cloudNotificationProvider": "1",
            "deviceId": "25b794-29a-4acb-9485-5a643d231f8U",
            "deviceLocationDateTime": "2017-04-18T05:37:59.932Z",
            "issuerId": "123457",
            "provider": "1",
            "source": "1"
        }
        
        data = LocationsModel(**data_kwargs)
        result = locations.send(data)
        print(result)
    """
    c = VisaMobileLocationConfirmationDispatcher(api='locationupdate', method='locations', data=data)
    return c.send()
