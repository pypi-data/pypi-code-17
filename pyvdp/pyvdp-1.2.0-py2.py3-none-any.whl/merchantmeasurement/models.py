import time

from datetime import datetime


class MerchantBenchmarkModel(object):
    """MerchantBenchmark data object model for Merchant Measurement APIs.
    
    :param pyvdp.merchantmeasurement.MerchantBenchmarkModel.RequestHeader requestHeader: **Optional**. 
        Instance of :func:`~pyvdp.merchantmeasurement.MerchantBenchmarkModel.RequestHeader`
    :param pyvdp.merchantmeasurement.MerchantBenchmarkModel.RequestData requestData: **Required**.
        Instance of :func:`~pyvdp.merchantmeasurement.MerchantBenchmarkModel.RequestData`
    
    **Request:**
    
    ..  code:: json
    
        {
            "requestHeader": {
                "messageDateTime": "2017-04-19T11:23:04.327Z",
                "requestMessageId": "6da60e1b8b024532a2e0eacb1af58581"
            },
            "requestData": {
                "merchantCategoryCodes": [
                    "5812"
                ],
                "merchantCategoryGroupsCodes": [""],
                "zipList": [
                    "77027"
                ],
                "msaList": [""],
                "countryList": [""],
                "monthList": [
                    "201501"
                ],
                "groupList": [
                    "standard"
                ],
                "cardPresentIndicator": "2"
            }
        }
           
    **Response:**
    
    TODO
    """
    ATTRS = [
        'requestHeader',
        'requestData'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    class RequestHeader(object):
        """Part of MerchantBenchmarkModel
        
        :param str requestMessageId: **Required**. Unique message identifier. If not provided, generated automatically. 
        """

        def __init__(self, **kwargs):
            self.messageDateTime = self._get_datetime()

            if kwargs and 'requestMessageId' in kwargs:
                self.requestMessageId = kwargs['requestMessageId']
            else:
                self.requestMessageId = self._get_message_id()

        @staticmethod
        def _get_datetime():
            date_format = '%Y-%m-%dT%H:%M:%S.%f'
            now = datetime.now()
            return now.strftime(date_format)[:-3]

        @staticmethod
        def _get_message_id():
            return 'Request_' + str(int(time.time()))

    class RequestData(object):
        """Data payload for MerchantBenchmarkModel.
        
        :param list merchantCategoryCodes: **Required**. A list of valid MCCs.
        :param list merchantCategoryGroupsCodes: **Required**. A list of valid merchant category group codes.
        :param list zipList: **Required**. A list of valid ZIP codes in USA.
        :param list msaList: **Required**. A list of valid metropolitan statistical areas in US.
        :param list countryList: **Required**. A list of valid countries. Currently only US is supported.
        :param list monthList: **Required**. A list of valid months in the format YYYYMM, e.g. 201605 for May.2016.
        :param list groupList: **Required**. Groups for which the end user is registered to the API. 
            Example- Standard/Cardholder or both.
        :param str cardPresentIndicator: **Optional**. Differentiator online from store transactions. Max 10 characters
            string.
        """
        ATTRS = [
            'merchantCategoryCodes',
            'merchantCategoryGroupsCodes',
            'zipList',
            'msaList',
            'countryList',
            'monthList',
            'groupList',
            'cardPresentIndicator'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
