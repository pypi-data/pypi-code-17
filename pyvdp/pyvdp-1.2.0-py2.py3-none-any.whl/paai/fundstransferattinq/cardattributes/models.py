from datetime import datetime
from pyvdp.paai import AbstractPaymentAccountAttributesInquiryModel


class FundsTransferInquiryModel(AbstractPaymentAccountAttributesInquiryModel):
    """Funds Transfer Inquiry data object model.

    :param str primaryAccountNumber: **Required**. Primary account number (PAN). 13-19 characters string.
    :param int systemsTraceAuditNumber: **Required**. Systems trace audit number.  6 digits integer.
    :param int acquiringBin: **Optional**. BIN under which FundsTransfer app is registered. 6-11 digits integer.
    :param int acquirerCountryCode: **Optional**. 3 digits acquirer country code.
    :param str retrievalReferenceNumber: **Optional**. RRN. If not provided, generated automatically based on STAN.
        12 characters string.

    **Request:**
    
    ..  code:: json

        {
            "primaryAccountNumber": "4957030420210512",
            "retrievalReferenceNumber": "330000550000",
                "systemsTraceAuditNumber": "451006"
        }
        
    **Response:**
    
    ..  code:: json
    
        {
            "cardTypeCode": "C",
            "billingCurrencyCode": "986",
            "billingCurrencyMinorDigits": 2,
            "issuerName": "Visa Test Bank",
            "cardIssuerCountryCode": "076",
            "fastFundsIndicator": "N",
            "pushFundsBlockIndicator": "N",
            "onlineGambingBlockIndicator": "Y"
        }    
    """
    ATTRS = [
        'systemsTraceAuditNumber',
        'primaryAccountNumber',
        'acquiringBin',
        'acquirerCountryCode',
        'retrievalReferenceNumber'
    ]

    def __init__(self, **kwargs):
        super(FundsTransferInquiryModel, self).__init__(**kwargs)

        try:
            self.retrievalReferenceNumber = kwargs['retrievalReferenceNumber']
        except KeyError:
            self.retrievalReferenceNumber = self._get_rrn()

        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    def _get_rrn(self):
        """Generates RRN (retrievalReferenceNumber).

        :return: str rrn: Last digit of current year + number of current day in the year + current hour + STAN
        """
        now = datetime.now()
        year_last_digit = now.strftime('%Y')[3]
        day_of_the_year = now.strftime('%j')
        current_hour = now.strftime('%H')
        return year_last_digit + day_of_the_year + current_hour + str(self.systemsTraceAuditNumber)
