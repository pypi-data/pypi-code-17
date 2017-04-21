from datetime import datetime


class AbstractInquiryModel(object):
    """Abstract base model for Global ATM Locator APIs.
    
    This class is not supposed to be instantiated on its own. Instead it should be implemented by concrete models.
    
    :param pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData requestData: **Required**. 
        Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData`.
    :param WsRequestHeaderV2 wsRequestHeaderV2: **Required**. 
        Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.WsRequestHeaderV2`.
    """
    ATTRS = [
        'requestData',
        'wsRequestHeaderV2',
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    class WsRequestHeaderV2(object):
        """Abstract request header.
        
        Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel`.
        
        Implemented by child classes as a part of their models.
        
        :param str applicationId: **Optional**. Application short name of the request originator.
        :param str requestMessageId: **Optional**. Request unique identifier.
        :param str correlationId: **Optional**. A string used to identify set of requests.
        :param str userId: **Optional**. User ID of the requesting user. May be '0' or 'NONE'.
        :param str userBid: **Optional**. Business User ID of the requesting user. May be '0' or 'NONE'.
        """
        ATTRS = [
            'applicationId',
            'requestMessageId',
            'correlationId',
            'userId',
            'userBid'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)

            self.requestTs = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

    class RequestData(object):
        """Abstract request data.
        
        Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel`.
        
        Implemented by child classes as a part of their models.
        
        :param str culture: **Optional**. A culture. Possible values: en-US.
        :param str distance: **Optional**. Search radius from initial point.
        :param str distanceUnit: **Optional**. Distance units for *distance* argument. Possible values: *mi*, *km*.
        :param Location location: **Required**. 
            Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Location`.
        :param Options options: **Required**.
            Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Options`.
        :param str metaDataOptions: **TODO: Undocumented**.
        """
        ATTRS = [
            'culture',
            'distance',
            'distanceUnit',
            'location',
            'options',
            'metaDataOptions'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)

        class Location(object):
            """Abstract Location data.
            
            Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData`.
            
            Implemented by child classes as a part of their models.
            
            :param str address: **TODO: Undocumented**.
            :param str placeName: **Conditional**. Single line address. Mandatory if Geocodes (latitude and/or 
                longitude) are not provided.
            :param Geocodes geocodes: **Conditional**. 
                Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Location.Geocodes`.
            """
            ATTRS = [
                'placeName',
                'geocodes'
            ]

            def __init__(self, **kwargs):
                for attr, value in kwargs.items():
                    if attr in self.ATTRS and value:
                        self.__setattr__(attr, value)

            class Geocodes(object):
                """Abstract Geocodes data.
                
                Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Location`.
                
                Implemented by child classes as a part of their models.
                
                :param int latitude: **Conditional**. Search center point latitude. Required if placeName is not
                    provided.
                :param int longitude: **Conditional**. Search center point longitude. Required if placeName is not
                    provided.
                """
                ATTRS = [
                    'latitude',
                    'longitude'
                ]

                def __init__(self, **kwargs):
                    for attr, value in kwargs.items():
                        if attr in self.ATTRS and value:
                            self.__setattr__(attr, value)

        class Options(object):
            """Abstract request options.
            
            Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData`.
            
            :param Range range: **Required**. 
                Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Options.Range`.
            :param Sort sort: **Required**.
                Instance of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Options.Sort`.
            :param str operationName: **Optional**. Logical operation to apply on findFilters. Possible values:
                *and*, *or*.
            :param list findFilters: **Optional**. A list of filters. 'Filter' is a dictionary with 'filterName' 
                and 'filterValue' pairs. See https://developer.visa.com/products/atmlocator/reference for details.
            :param bool useFirstAmbiguous: **TODO: Undocumented**.
            """
            ATTRS = [
                'range',
                'sort',
                'operationName',
                'findFilters',
                'useFirstAmbiguous'
            ]

            def __init__(self, **kwargs):
                for attr, value in kwargs.items():
                    if attr in self.ATTRS and value:
                        self.__setattr__(attr, value)

            class Range(object):
                """Abstract request range.
                
                Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Options`.
                
                :param int start: **Required**. Starting index of response records. E.g. *'0'*.
                :param int count: **Required**. A number of records to fetch. E.g. *'100'*.
                """
                ATTRS = [
                    'count',
                    'start'
                ]

                def __init__(self, **kwargs):
                    for attr, value in kwargs.items():
                        if attr in self.ATTRS and value:
                            self.__setattr__(attr, value)

            class Sort(object):
                """Abstract request sort.
                
                Part of :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel.RequestData.Options`.
                
                :param str primary: **Required**. Primary sort filter. Possible values: *distance*, *city*.
                :param str direction: **Required**. Sort direction. Possible values: *asc*, *desc*.
                :param str secondary: **Optional**. Secondary sort filter. Possible values: *distance*, *city*.
                """
                ATTRS = [
                    'direction',
                    'primary',
                    'secondary'
                ]

                def __init__(self, **kwargs):
                    for attr, value in kwargs.items():
                        if attr in self.ATTRS and value:
                            self.__setattr__(attr, value)


class AtmsInquiryModel(AbstractInquiryModel):
    """ATMs Inquiry data object model.
    
    See :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel`.
    
    **Request:**
    
    ..  code:: json
    
        {
            "requestData": {
                "culture": "en-US",
                "distance": "20",
                "distanceUnit": "mi",
                "location": {
                    "address": null,
                    "geocodes": null,
                    "placeName": "800 metro center , foster city,ca"
                },
                "metaDataOptions": 0,
                "options": {
                    "findFilters": [
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
                    ],
                    "operationName": "or",
                    "range": {
                        "count": 99,
                        "start": 0
                    },
                    "sort": {
                        "direction": "desc",
                        "primary": "city"
                    },
                    "useFirstAmbiguous": true
                }
            },
            "wsRequestHeaderV2": {
                "applicationId": "VATMLOC",
                "correlationId": "909420141104053819418",
                "requestMessageId": "test12345678",
                "requestTs": "2017-04-19T05:45:57.000Z",
                "userBid": "10000108",
                "userId": "CDISIUserID"
            }
        }
                
    **Response:**
    
    ..  code:: json
    
        {
            "responseData": [
                {
                    "bestMapView": null,
                    "totalATMCount": 0,
                    "metaData": null,
                    "matchedLocations": [
                        {
                            "location": {
                                "placeName": "800 Metro Center Blvd, Foster City, California, 94404",
                                "score": 90.92,
                                "geocodeMethod": null,
                                "coordinates": {
                                    "latitude": 37.55847628805134,
                                    "longitude": -122.27828269468989
                                },
                                "address": {
                                    "street": "800 Metro Center Blvd",
                                    "street2": "",
                                    "postalCode": "94404",
                                    "city": "Foster City",
                                    "formattedAddress": "800 Metro Center Blvd, Foster City, California, 94404",
                                    "state": "California",
                                    "country": "USA"
                                },
                                "typeName": "PointAddress",
                                "properties": null
                            }
                        }
                    ],
                    "foundATMLocations": null,
                    "distanceUnit": null,
                    "properties": null
                }
            ],
            "wsResponseHeader": null,
            "wsStatus": {
                "statusDesc": "Visa ATM Locator Svc-Failure (Empty Response Received from GMR)",
                "statusCode": "CDIS203"
            },
            "wsResponseHeaderV2": {
                "responseTs": 1492581295522,
                "correlationId": "909420141104053819418",
                "requestMessageId": "test12345678",
                "responseMessageId": "51VATMLOC169720170419055454794",
                "numOfRowsReturned": 0
            },
            "responseSummaryData": null
        }    
    """
    def __init__(self, **kwargs):
        super(AtmsInquiryModel, self).__init__(**kwargs)


class TotalsInquiryModel(AbstractInquiryModel):
    """Totals Inquiry data object model.

    See :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel`.
    
    **Request:**
    
    ..  code:: json

        {
            "requestData": {
                "culture": "en-US",
                "distance": "20",
                "distanceUnit": "mi",
                "location": {
                    "address": null,
                    "geocodes": null,
                    "placeName": "800 metro center , foster city,ca"
                },
                "metaDataOptions": 0,
                "options": {
                    "findFilters": [
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
                    ],
                    "operationName": "or",
                    "range": {
                        "count": 99,
                        "start": 0
                    },
                    "sort": {
                        "direction": "desc",
                        "primary": "city"
                    },
                    "useFirstAmbiguous": true
                }
            },
            "wsRequestHeaderV2": {
                "applicationId": "VATMLOC",
                "correlationId": "909420141104053819418",
                "requestMessageId": "test12345678",
                "requestTs": "2017-04-19T06:37:19.000Z",
                "userBid": "10000108",
                "userId": "CDISIUserID"
            }
        }
           
    **Response:**
    
    ..  code:: json
    
        {
            "wsResponseHeader": null,
            "wsStatus": {
                "statusDesc": "Visa ATM Locator Svc-Failure (Empty Response Received from GMR)",
                "statusCode": "CDIS203"
            },
            "wsResponseHeaderV2": {
                "requestMessageId": "test12345678",
                "responseMessageId": "51VATMLOC8954820170419063914015",
                "correlationId": "909420141104053819418",
                "numOfRowsReturned": 0,
                "responseTs": 1492583954720
            },
            "responseSummaryData": null,
            "responseData": [
                {
                    "metaData": null,
                    "matchedLocations": [
                        {
                            "location": {
                                "score": 90.92,
                                "placeName": "800 Metro Center Blvd, Foster City, California, 94404",
                                "geocodeMethod": null,
                                "coordinates": {
                                    "latitude": 37.55847628805134,
                                    "longitude": -122.27828269468989
                                },
                                "address": {
                                    "city": "Foster City",
                                    "formattedAddress": "800 Metro Center Blvd, Foster City, California, 94404",
                                    "street": "800 Metro Center Blvd",
                                    "street2": "",
                                    "postalCode": "94404",
                                    "state": "California",
                                    "country": "USA"
                                },
                                "typeName": "PointAddress",
                                "properties": null
                            }
                        }
                    ],
                    "foundATMLocations": null,
                    "distanceUnit": null,
                    "totalATMCount": 0,
                    "bestMapView": null,
                    "properties": null
                }
            ]
        }    
    """
    def __init__(self, **kwargs):
        super(TotalsInquiryModel, self).__init__(**kwargs)


class GeocodesInquiryModel(AbstractInquiryModel):
    """Geocodes Inquiry data object model.

    See :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel`.
    
    **Request:**
    
    ..  code:: json
    
        {
            "requestData": {
                "culture": null,
                "distance": "20",
                "distanceUnit": "mi",
                "location": {
                    "address": null,
                    "geocodes": null,
                    "placeName": "San Raphael"
                },
                "metaDataOptions": 0,
                "options": {
                    "fetchATMOwnerData": "Y",
                    "findFilters": [
                        {
                            "filterName": "CHIP_ENABLED",
                            "filterValue": 1
                        },
                        {
                            "filterName": "ACCESS_HOURS",
                            "filterValue": "B"
                        }
                    ],
                    "range": {
                        "count": 99,
                        "start": 0
                    },
                    "sort": {
                        "direction": "asc",
                        "primary": "distance"
                    },
                    "useFirstAmbiguous": true
                }
            },
            "wsRequestHeaderV2": {
                "applicationId": "GEOCODE",
                "correlationId": "909420141104053819418",
                "requestMessageId": "ICE01-001",
                "requestTs": "2017-04-19T06:04:14.000Z",
                "userBid": "10000108",
                "userId": "CDISIUserID"
            }
        } 
           
    **Response:**
    
    ..  code:: json
    
        {
            "wsStatus": {
                "statusDesc": "Geocoding Svc-Success",
                "statusCode": "CDI000"
            },
            "responseSummaryData": null,
            "wsResponseHeader": null,
            "wsResponseHeaderV2": {
                "numOfRowsReturned": 5,
                "requestMessageId": "ICE01-001",
                "correlationId": "909420141104053819418",
                "responseMessageId": "56GEOCODE1127320170419060550997",
                "responseTs": 1492581951544
            },
            "responseData": [
                {
                    "FoundATMLocations": null,
                    "DistanceUnit": null,
                    "MatchedLocations": [
                        {
                            "Score": 100,
                            "Location": {
                                "Coordinates": {
                                    "Latitude": -22.724516672999584,
                                    "Longitude": -47.650647644999594
                                },
                                "BestViewMap": null,
                                "GeocodeMethod": null,
                                "PlaceName": "San Raphael",
                                "Address": {
                                    "PostalCode": "",
                                    "FormattedAddress": null,
                                    "Street": "Rua Moraes Barros",
                                    "Street2": "Centro",
                                    "City": "Piracicaba",
                                    "State": "Sudeste",
                                    "Country": "BRA"
                                },
                                "TypeName": "POI",
                                "Property": null
                            }
                        },
                        { ... },
                        { ... }
                    ],
                    "BestViewMap": null,
                    "MetaData": null,
                    "Properties": null
                }
            ]
        }    
    """
    def __init__(self, **kwargs):
        super(GeocodesInquiryModel, self).__init__(**kwargs)


class RoutesInquiryModel(AbstractInquiryModel):
    """Routes Inquiry data object model.

    See :func:`~pyvdp.globalatmlocator.localatms.AbstractInquiryModel`.
    
    **Request:**
    
    ..  code:: json
    
        {
            "requestData": {
                "doNotLocateOnRestrictedElements": true,
                "features": [
                    {
                        "geometry": {
                            "x": -122.4079,
                            "y": 37.78356
                        }
                    },
                    {
                        "geometry": {
                            "x": -122.404,
                            "y": 37.782
                        }
                    }
                ],
                "travelMode": {
                    "type": "WALKINGTIME"
                },
                "type": "features"
            },
            "wsRequestHeaderV2": {
                "applicationId": "GEOCODE",
                "correlationId": "909420141104053819418",
                "requestMessageId": "ICE01-001",
                "requestTs": "2017-04-19T06:20:56.000Z",
                "userBid": "10000108",
                "userId": "CDISIUserID"
            }
        }
            
    **Response:**
    
    ..  code:: json
    
        {
            "wsStatus": {
                "statusDesc": "Geocoding Svc-Success",
                "statusCode": "CDI000"
            },
            "responseSummaryData": null,
            "wsResponseHeader": null,
            "wsResponseHeaderV2": {
                "numOfRowsReturned": 1,
                "requestMessageId": "ICE01-001",
                "correlationId": "909420141104053819418",
                "responseMessageId": "56GEOCODE8894420170419062221743",
                "responseTs": 1492582942222
            },
            "responseData": [
                {
                    "routes": {
                        "geometryType": "esriGeometryPolyline",
                        "fieldAliases": {
                            "ObjectID": "ObjectID",
                            "Name": "Name",
                            "FirstStopID": "FirstStopID",
                            "LastStopID": "LastStopID",
                            "StopCount": "StopCount",
                            "Total_Kilometers": "Total_Kilometers",
                            "Total_Miles": "Total_Miles",
                            "Total_WalkTime": "Total_WalkTime",
                            "Total_TravelTime": null,
                            "Shape_Length": "Shape_Length"
                        },
                        "features": [
                            {
                                "geometry": {
                                    "paths": [
                                        [
                                            [
                                                -122.40774845199996,
                                                37.783745569000075
                                            ],
                                            [
                                                -122.40745999999996,
                                                37.783510000000035
                                            ],
                                            [
                                                -122.40722999999997,
                                                37.78334000000007
                                            ],
                                            [
                                                -122.40718999999996,
                                                37.78331000000003
                                            ],
                                            [
                                                -122.40699999999998,
                                                37.783160000000066
                                            ],
                                            [
                                                -122.40648999999996,
                                                37.78274000000005
                                            ],
                                            [
                                                -122.40591999999998,
                                                37.78230000000008
                                            ],
                                            [
                                                -122.40545999999995,
                                                37.78195000000005
                                            ],
                                            [
                                                -122.40492999999998,
                                                37.781510000000026
                                            ],
                                            [
                                                -122.40411865599998,
                                                37.78215034300007
                                            ]
                                        ]
                                    ]
                                },
                                "attributes": {
                                    "ObjectID": 1,
                                    "Name": "Location 1 - Location 2",
                                    "FirstStopID": 1,
                                    "LastStopID": 2,
                                    "StopCount": 2,
                                    "Total_Kilometers": 0.45227018911150985,
                                    "Total_Miles": 0.2810276666216233,
                                    "Total_WalkTime": 5.427242269338118,
                                    "Total_TravelTime": 0,
                                    "Shape_Length": 0.004631701407551423
                                }
                            }
                        ],
                        "spatialReference": {
                            "wkid": 4326,
                            "latestWkid": 4326
                        }
                    },
                    "directions": [
                        {
                            "routeId": 1,
                            "routeName": "Location 1 - Location 2",
                            "features": [
                                {
                                    "compressedGeometry": "+bd6bc-1bkv4en+df6i90+0+0",
                                    "attributes": { }
                                },
                                {
                                    "compressedGeometry": "+bd6bc-1bkv4en+df6i90+3bs-2o3+2m1-1vi+eu-b7+272-1o3+5un-4t2+6l5-54h+5c1-42t+666-54h",
                                    "attributes": {
                                        "length": 0.21836241630617984,
                                        "time": 4.217006249208293,
                                        "text": "Go southeast on 5th St toward Stevenson St",
                                        "maneuverType": "esriDMTStraight",
                                        "ETA": -2209161600000
                                    }
                                },
                                {
                                    "compressedGeometry": "+bd6bc-1bku3gn+df5o50+9fe+7ff",
                                    "attributes": {
                                        "length": 0.06266769505165845,
                                        "time": 1.2102360201298248,
                                        "text": "Turn left on Howard St",
                                        "maneuverType": "esriDMTTurnLeft",
                                        "ETA": -2209161600000
                                    }
                                },
                                {
                                    "compressedGeometry": "+bd6bc-1bktq19+df5vkf+0+0",
                                    "attributes": { }
                                }
                            ],
                            "summary": {
                                "totalLength": 0.2810301113578383,
                                "totalTime": 5.427242269506678,
                                "envelope": {
                                    "ymin": 37.781510000000026,
                                    "ymax": 37.78374556907189,
                                    "xmin": -122.40789999999998,
                                    "xmax": -122.40399999999994,
                                    "spatialReference": {
                                        "wkid": 4326,
                                        "latestWkid": 4326
                                    }
                                },
                                "totalDriveTime": 5.427242269338118
                            }
                        }
                    ],
                    "messages": [ ]
                }
            ]
        }    
    """
    def __init__(self, **kwargs):
        super(RoutesInquiryModel, self).__init__(**kwargs)

    class RequestData(object):
        """Routes Inquiry request data object model.
        
        Part of :func:`~pyvdp.globalatmlocator.localatms.RoutesInquiryModel`.
        
        :param bool doNotLocateOnRestrictedElements: **TODO: Undocumented**.
        :param list features: **TODO: Undocumented**. 
            A list of :func:`~pyvdp.globalatmlocator.localatms.RoutesInquiryModels.RequestData.Geometry` objects.
        :param pyvdp.globalatmlocator.localatms.RoutesInquiryModels.RequestData.TravelMode travelMode:
            **TODO: Undocumented**.
        :param str type: **TODO: Undocumented**.
        """
        ATTRS = [
            'doNotLocateOnRestrictedElements',
            'features',
            'travelMode',
            'type'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)

        class Geometry(object):
            """Geometry data object model.
            
            Part of :func:`~pyvdp.globalatmlocator.localatms.RoutesInquiryModel.RequestData`.
            
            :param float x: **Required**. X-coordinate. E.g. -122.4079.
            :param float y: **Required**. Y-coordinate. E.g. 37.782
            """
            ATTRS = [
                'x',
                'y'
            ]

            def __init__(self, **kwargs):
                for attr, value in kwargs.items():
                    if attr in self.ATTRS and value:
                        self.__setattr__(attr, value)

        class TravelMode(object):
            """Geocodes request travel mode data object model.
            
            Part of :func:`~pyvdp.globalatmlocator.localatms.RoutesInquiryModel.RequestData`.
            
            :param str type: **TODO: Undocumented**.
            """
            ATTRS = [
                'type'
            ]

            def __init__(self, **kwargs):
                for attr, value in kwargs.items():
                    if attr in self.ATTRS and value:
                        self.__setattr__(attr, value)
