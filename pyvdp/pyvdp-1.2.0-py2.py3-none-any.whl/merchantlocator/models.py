import time

from datetime import datetime


class LocatorModel(object):
    """Locator data object model for Merchant Locator APIs.
    
    :param pyvdp.merchantlocator.LocatorModel.Header header: **Optional**. 
        Instance of :func:`~pyvdp.merchantlocator.MerchantLocatorModel.Header`.
        If not provided, will be set automatically. See docs for Header subclass.
    :param SearchAttrList searchAttrList: **Required**. 
        Instance of :func:`~pyvdp.merchantlocator.LocatorModel.SearchAttrList`.
    :param list responseAttrList: **Required**. A list of response attributes.
    :param SearchOptions searchOptions: **Required**. 
        Instance of :func:`~pyvdp.merchantlocator.LocatorModel.SearchOptions`.
        
    **Request:**
    
    ..  code:: json

        {
            "header": {
                "messageDateTime": "2017-04-19T10:46:43.903",
                "requestMessageId": "Request_001",
                "startIndex": "0"
            },
            "searchAttrList": {
                "merchantName": "Starbucks",
                "merchantCountryCode": "840",
                "latitude": "37.363922",
                "longitude": "-121.929163",
                "distance": "2",
                "distanceUnit": "M"
            },
            "responseAttrList": [
                "GNLOCATOR"
            ],
            "searchOptions": {
                "maxRecords": "5",
                "matchIndicators": "true",
                "matchScore": "true"
            }
        }
            
    **Response:**
    
    ..  code:: json
    
        {
            "merchantLocatorServiceResponse": {
            "response": [
                {
                    "responseValues": {
                        "businessLegalName": [
                            "HMS HOST CORPORATION"
                        ],
                        "paymentFacilitatorName": [ ],
                        "merchantCategoryCodeDesc": [
                            "FAST FOOD RESTAURANTS"
                        ],
                        "visaEnterpriseName": "STARBUCKS",
                        "8AClassified": "N",
                        "primaryMerchantCategoryCode": "",
                        "visaPartnerProgramMerchant": [ ],
                        "merchantCountryCode": "840",
                        "merchantStreetAddress": "1661 AIRPORT BLVD # 3E",
                        "merchantPostalCode": "95110-1216",
                        "merchantState": "CA",
                        "merchantCity": "SAN JOSE",
                        "paymentAcceptanceMethod": [
                            "F2F"
                        ],
                        "terminalType": [
                            "SWIPE"
                        ],
                        "merchantCategoryCode": [
                            "5814"
                        ],
                        "fleetIndicator": "",
                        "level2Indicator": "N",
                        "level3SummaryIndicator": "N",
                        "level3LineItemIndicator": "N",
                        "disabledVeteranOwned": "N",
                        "hubzoneCertified": "N",
                        "minorityOwned": "N",
                        "sbaregistered": "N",
                        "veteranOwned": "N",
                        "smallDisadvantagedBusiness": "N",
                        "vietnamVeteranOwned": "N",
                        "womenOwned": "N",
                        "distance": "0.4 m",
                        "visaMerchantName": "STARBUCKS",
                        "visaStoreName": "STARBUCKS",
                        "locationAddressLatitude": "37.363363",
                        "locationAddressLongitude": "-121.921986",
                        "visaStoreId": "177066014",
                        "visaMerchantId": "29992901",
                        "merchantUrl": [ ],
                        "dbaname": [
                            "NC 1 STARBUCKS30101539",
                            "TA STARBUCKS  30101505",
                            "NC 5 STARBUCKS30101547",
                            "STARBUCKS TERM30101554"
                        ]
                    },
                    "matchIndicators": {
                        "merchantCountryCode": "Y",
                        "merchantName": "Y"
                    },
                    "matchScore": "0.96228695"
                },
                { ... },
                { ... }
            ],
            "header": {
                "startIndex": "0",
                "numRecordsMatched": 3,
                "numRecordsReturned": 3,
                "requestMessageId": "Request_001",
                "messageDateTime": "2017-04-19T10:47:34.651",
                "responseMessageId": "68VDP3366620170419104734651",
                "endIndex": "2"
            },
            "status": {
                "statusDescription": "Success",
                "statusCode": "CDI000"
            }
            }
        }    
    """
    ATTRS = [
        'header',
        'searchAttrList',
        'responseAttrList',
        'searchOptions'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

        if 'header' not in kwargs:
            self.header = LocatorModel.Header()

    class Header(object):
        """Merchant Locator request header object.
        
        Part of LocatorModel object.
        
        :param str requestMessageId: **Optional**. Unique request identifier. If not provided, generated automatically.
        :param int startIndex: **Optional**. Starting index in response object. Default 0.
        """

        def __init__(self, **kwargs):
            self.messageDateTime = self._get_datetime()

            if kwargs and 'requestMessageId' in kwargs:
                self.requestMessageId = kwargs['requestMessageId']
            else:
                self.requestMessageId = self._get_message_id()

            if kwargs and 'startIndex' in kwargs:
                self.startIndex = kwargs['startIndex']
            else:
                self.startIndex = 0

        @staticmethod
        def _get_datetime():
            date_format = '%Y-%m-%dT%H:%M:%S.%f'
            now = datetime.now()
            return now.strftime(date_format)[:-3]

        @staticmethod
        def _get_message_id():
            return 'Request_' + str(int(time.time()))

    class SearchAttrList(object):
        """Merchant Locator search attributes object.
        
        Part of LocatorModel object.
        
        :param str merchantName: **Conditional**. Name of the merchant. Not required if MCC or phone number provided.
        :param str merchantCategoryCode: **Conditional**. Merchant category code or codes. Not required if merchant
            name or phone number provided. Can be a list of comma-separated values.
        :param int merchantCountryCode: **Required**. Merchant country ISO code. 3 characters string.
        :param int distance: **Required**. Distance value. Integer in 0-100 range.
        :param str distanceUnit: **Required**. Distance unit. M or KM.
        :param str merchantStreetAddress: **Optional**. Merchant street address.
        :param str merchantCity: **Optional**. Merchant city name. 
        :param str merchantState: **Optional**. Merchant state code.
        :param str merchantPostalCode: **Conditional**. Merchant postal code. Must not be provided if latitude and
            longitude are set.
        :param str longitude: **Conditional**. Longitude value between -180 and +180. Must not be provided if postal 
            code is set.
        :param str latitude: **Conditional**. Latitude value between -90 and +90. Must not be provided if postal 
            code is set. 
        :param int merchantPhoneNumber: **Optional**. Phone number of the registered Merchant.
        """
        ATTRS = [
            'merchantName',
            'merchantCategoryCode',
            'merchantCountryCode',
            'distance',
            'distanceUnit',
            'merchantStreetAddress',
            'merchantCity',
            'merchantState',
            'merchantPostalCode',
            'longitude',
            'latitude',
            'merchantPhoneNumber'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)

    class SearchOptions(object):
        """Merchant locator search options object.
        
        Part of LocatorModel object.
        
        :param int maxRecords: **Optional**. Maximum number of records in the response. Default 25.
        :param bool matchIndicators: **Optional**. If set to True, matching request attributes will be included in 
            response.
        :param bool matchScore: **Optional**. If set to True, matching score will be included in response.
        :param str proximity: **Optional**. A proximity search tag on merchant name. Ignored if wildcard is provided.
        :param str wildcard: **Optional**. A wildcard search on merchant name.
        """
        ATTRS = [
            'maxRecords',
            'matchIndicators',
            'matchScore',
            'proximity',
            'wildcard'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
