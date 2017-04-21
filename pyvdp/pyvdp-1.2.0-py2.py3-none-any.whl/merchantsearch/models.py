import time

from datetime import datetime


class SearchModel(object):
    """Visa Merchant Search data object model.
    
    :param MerchantSearchHeader header: **Required**. 
        Instance of :func:`~pyvdp.merchantsearch.SearchModel.MerchantSearchHeader`
    :param MerchantSearchAttrList searchAttrList: **Required**. 
        Instance of :func:`~pyvdp.merchantsearch.SearchModel.MerchantSearchAttrList`
    :param list responseAttrList: **Required**. A list with attributes (Group Names) to include in response.
    :param MerchantSearchOptions searchOptions: **Required**.
        Instance of :func:`~pyvdp.merchantsearch.SearchModel.MerchantSearchOptions`

    **Request:**
    
    ..  code:: json

        {
            "header": {
                "messageDateTime": "2017-03-18T03:39:08.903",
                "requestMessageId": "Request_001",
                "startIndex": "0"
            },
            "searchAttrList": {
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
            },
            "responseAttrList": [
                "GNSTANDARD"
            ],
            "searchOptions": {
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
        }
        
    **Response:**
    
    ..  code:: json
    
        {
            "merchantSearchServiceResponse": {
                "response": [
                    {
                        "responseValues": {
                            "merchantStreetAddress": "802 INDUSTRIAL DR",
                            "merchantCity": "MOUNT PLEASANT",
                            "merchantState": "MI",
                            "merchantPostalCode": "48858-4646",
                            "visaStoreName": "SCHOOL OF EXTENDED LEARNING",
                            "visaMerchantName": "CMU EDCTN MATERIALS CN",
                            "dbaname": [
                                "CMU GLOBAL CAMPUS ADMISS",
                                "CMU EDCTN MATERIALS CNTR",
                                "CMU GLOBAL CAMPUS PROGMS",
                                "CMU GLOBAL CAMPUS NONCRD",
                                "CMU GLOBAL CAMPUS PYMNTS"
                            ],
                            "businessLegalName": [
                                "CENTRAL MICHIGAN UNIV",
                                "CENTRAL MICHIGAN UNIVERSITY",
                                "CENTRAL MICHIGAN UNVRSTY"
                            ],
                            "paymentFacilitatorName": [],
                            "visaEnterpriseName": "CMU",
                            "merchantCategoryCode": [
                                "8220"
                            ],
                            "merchantCategoryCodeDesc": [
                                "COLLEGES/UNIV/JC/PROFESSION"
                            ],
                            "paymentAcceptanceMethod": [
                                "F2F",
                                "EC",
                                "MOTO"
                            ],
                            "terminalType": [
                                "SWIPE"
                            ],
                            "firstTranDateRange": "In more than 365 days",
                            "lastTranDateRange": "In last 365 days",
                            "fleetIndicator": "",
                            "level2Indicator": "Y",
                            "level3SummaryIndicator": "Y",
                            "level3LineItemIndicator": "N",
                            "disabledVeteranOwned": "N",
                            "hubzoneCertified": "N",
                            "minorityOwned": "N",
                            "sbaregistered": "N",
                            "veteranOwned": "N",
                            "smallDisadvantagedBusiness": "N",
                            "vietnamVeteranOwned": "N",
                            "womenOwned": "N",
                            "merchantPhoneNumber": [
                                {
                                    "type": "O",
                                    "number": "9897747123"
                                },
                                {
                                    "type": "O",
                                    "number": "8006642681"
                                },
                                {
                                    "type": "O",
                                    "number": "8772684636"
                                },
                                {
                                    "type": "O",
                                    "number": "9897743986"
                                },
                                {
                                    "type": "O",
                                    "number": "9897747121"
                                }
                            ],
                            "visaMerchantId": "34619535",
                            "visaStoreId": "166156429",
                            "merchantUrl": [ ],
                            "merchantCountryCode": "840",
                            "8AClassified": "N",
                            "primaryMerchantCategoryCode": "",
                            "visaPartnerProgramMerchant": [ ]
                        },
                        "matchIndicators": {
                            "merchantStreetAddress": "Y",
                            "merchantCity": "Y",
                            "merchantState": "Y",
                            "merchantPostalCode": "Y",
                            "merchantName": "Y",
                            "acquirerCardAcceptorId": "N",
                            "acquiringBin": "N",
                            "merchantPhoneNumber": "N",
                            "businessRegistrationId": "N",
                            "merchantUrl": "N",
                            "merchantCountryCode": "Y"
                        },
                        "matchScore": "2.344385"
                    }
                ],
                "header": {
                    "responseMessageId": "64VDP877520170419115525215",
                    "startIndex": "0",
                    "numRecordsMatched": 1,
                    "numRecordsReturned": 1,
                    "requestMessageId": "Request_001",
                    "messageDateTime": "2017-04-19T11:55:25.215",
                    "endIndex": "0"
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

    class MerchantSearchHeader(object):
        """MerchantSearch header data object model.

        Part of MerchantSearch object.

        :param str requestMessageId: **Optional**. Unique string ID. String 50 characters max. 
        :param int startIndex: **Optional**. Starting records index in response.
        """

        def __init__(self, **kwargs):
            self.messageDateTime = self._get_datetime()

            if kwargs and 'requestMessageId' in kwargs:
                self.requestMessageId = kwargs['requestMessageId']
            else:
                self.requestMessageId = self._get_message_id()

            if kwargs and 'startIndex' in kwargs.items():
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

    class MerchantSearchAttrList(object):
        """MerchantSearch searchAttrList data object model.

        Part of MerchantSearch object.

        :param str merchantName: **Conditional**. Name of the merchant. Optional when any one of VisaMerchantId or
            VisaStoreId or BusinessRegistrationId or MerchantUrl or AcquirerCardAcceptorId is provided.
        :param str merchantStreetAddress: **Conditional**. Merchant street address.
        :param str merchantCity: **Conditional**. City of the registered merchant.
        :param str merchantState: **Conditional**. Merchant state code. 2 characters string.
        :param str merchantPostalCode: **Conditional**. Merchant postal code.
        :param int merchantCountryCode: **Conditional**. Merchant country code, mandatory with merchant_name.
        :param int merchantPhoneNumber: **Conditional**. Merchant phone number.
        :param str merchantUrl: **Conditional**. Merchant registered URL. Optional when any one of MerchantName or
            VisaMerchantId or VisaStoreId or BusinessRegistrationId or AcquirerCardAcceptorId is provided.
        :param int visaMerchantId: **Conditional**. Merchant ID provided by VISA. Optional when any one of MerchantName
            or VisaStoreId or BusinessRegistrationId or MerchantUrl or AcquirerCardAcceptorId is provided. 8 characters
            double.
        :param int visaStoreId: **Conditional**. Merchant store/branch ID, provided by VISA. Optional when any one of
            MerchantName or VisaMerchantId or BusinessRegistrationId or MerchantUrl or AcquirerCardAcceptorId is provided.
            9 characters double.
        :param str businessRegistrationId: **Conditional**. Merchant business/tax registration ID. Optional when any
            one of merchantName or visaMerchantId or visaStoreId or merchantUrl or acquirerCardAcceptorId is provided.
        :param str merchant_url: **Required**. Merchant registered URL. Optional when any one of merchantName or
            visaMerchantId or visaStoreId or businessRegistrationId or acquirerCardAcceptorId is provided.
        :param str acquirerCardAcceptorId: **Required**. Acquirer card acceptor ID. Optional when any one of
            merchantName or visaMerchantId or visaStoreId or businessRegistrationId or merchantUrl is provided. 15 digits
            string. Prepend 0 if less than 15 digits.
        :param int acquiringBin: **Required**. Acquirer business identification number. Required when
            acquirerCardAcceptorId is provided.
        """

        ATTRS = [
            'merchantName',
            'merchantStreetAddress',
            'merchantCity',
            'merchantState',
            'merchantPostalCode',
            'merchantCountryCode',
            'merchantPhoneNumber',
            'merchantUrl',
            'visaMerchantId',
            'visaStoreId',
            'businessRegistrationId',
            'acquirerCardAcceptorId',
            'acquiringBin',
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)

    class MerchantSearchOptions(object):
        """MerchantSearch searchOptions data object model.

        Part of MerchantSearch data object.

        :param int maxRecords: **Optional**. Maximum number of records in response. Default 25.
        :param bool matchIndicators: **Optional**. Show request attributes, that match a record.
        :param bool matchScore: **Optional**. Add matchScore and order response per matchScore.
        :param list proximity: **Optional**. Proximity search on merchant name. If wildcards are used, proximity is 
            ignored.
        :param list wildcards: **Optional**. Wildcard search on merchant name.
        """

        ATTRS = [
            'maxRecords',
            'matchIndicators',
            'matchScore',
            'proximity',
            'wildcards'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
