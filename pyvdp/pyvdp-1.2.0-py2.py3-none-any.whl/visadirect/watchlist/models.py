import string
import random


class WatchListInquiryModel(object):
    """VisaDirect WatchlistScreening WatchlistInquiry data object model.

    :param str name: **Required**. Name of the person, to receive WLM score. Max 255 characters latin string.
    :param WatchListInquiryAddress address: **Required**. Instance of :func:`~pyvdp.visadirect.watchlist.WatchListInquiryModel.WatchListInquiryAddress`.
    :param int acquiringBin: **Conditional**.  This field is required if acquirerCountryCode field is provided. Bank
        Identification Number provided during enrollment. 6-11 digits integer.
    :param int acquirerCountryCode: **Optional**. Acquirer ISO country code, provided during enrollment. 3 digits
        integer

    **Request:**
    
    ..  code:: json
    
        {
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "address": {
                "cardIssuerCountryCode": "USA",
                "city": "San Francisco"
            },
            "name": "Mohammed Qasim",
            "referenceNumber": "330000550000"
        }
            
    **Response:**
    
    ..  code:: json
    
        {
            "referenceNumber": "330000550000",
            "ofacScore": "10",
            "status": "Approved"
        }    
    """
    ATTRS = [
        'name',
        'address',
        'acquiringBin',
        'acquirerCountryCode',
    ]

    def __init__(self, **kwargs):

        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

        self.referenceNumber = self.__get_reference()

    @staticmethod
    def __get_reference():
        """Generates random 12-digit reference to tie together a WLM score request and WLM score response service calls.

        :return: reference
        """
        return ''.join(random.choice(string.digits) for _ in range(12))

    class WatchListInquiryAddress(object):
        """Watchlist address object model, part of :func:`~pyvdp.visadirect.watchlist.WatchListInquiryModel`.
    
        :param str city: **Required**. Client city name.
        :param str cardIssuerCountryCode: **Required**. Card issuer 3 characters ISO country code.
        """
        ATTRS = [
            'city',
            'cardIssuerCountryCode'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
