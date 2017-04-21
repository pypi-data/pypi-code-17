from datetime import datetime

try:
    import configparser as parser
except ImportError:
    import ConfigParser as parser

transaction_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


class VisaDirectTransactionModel(object):
    """Abstract VISA Transaction object model.

    Constructs and populates general attributes, such as systemsTraceAuditNumber (stan), retrievalReferenceNumber
    (rrn) and localTransactionDateTime.

    :param str stan: **Required**. Systems Trace Audit Number (STAN), 6 digits integer.
    """
    def __init__(self, **kwargs):
        self.systemsTraceAuditNumber = kwargs['systemsTraceAuditNumber']
        self.localTransactionDateTime = transaction_datetime

        if kwargs and 'retrievalReferenceNumber' in kwargs:
            self.retrievalReferenceNumber = kwargs['retrievalReferenceNumber']
        else:
            self.retrievalReferenceNumber = self._get_rrn()

    def _get_rrn(self):
        """Generates RRN (retrievalReferenceNumber).

        :return: str rrn: Last digit of current year + number of current day in the year + current hour + STAN
        """
        now = datetime.now()
        year_last_digit = now.strftime('%Y')[3]
        day_of_the_year = now.strftime('%j')
        current_hour = now.strftime('%H')

        return year_last_digit + day_of_the_year + current_hour + str(self.systemsTraceAuditNumber)


class VisaDirectTransactionBatchModel(object):
    """Abstract TransactionBatch object model.

    Constructs and populates a 'transaction of transactions', normally submitted with `multi` requests.
    This class is not supposed to be instantiated on its own, it is just providing a `shell` for batch requests

    :param list request: **Required**. List of :func:`~pyvdp.visadirect.VisaDirectTransactionModel` objects.
    """
    def __init__(self, request):
        self.localTransactionDateTime = transaction_datetime
        self.request = request


class CardAcceptorModel(object):
    """Card Acceptor object model.

    :param str name: **Required**. Name of the originator or money transfer operator. Max 25 characters string.
    :param str terminalId: **Required**. Identifier of the terminal at a card acceptor location. Max 8 characters
        string.
    :param str idCode: **Required**. Identifier of card acceptor (Visa Direct Originator). Max 15 characters string.
    :param dict address: **Required**. See :func:`~pyvdp.visadirect.CardAcceptorModel.CardAcceptorAddress` class for 
        allowed keys.
    """
    ATTRS = [
        'name',
        'terminalId',
        'idCode',
        'address'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    class CardAcceptorAddress(object):
        """Card Acceptor address object model (part of :func:`~pyvdp.visadirect.CardAcceptorModel` object).

        Populated from `address` dictionary argument for :func:`~pyvdp.visadirect.CardAcceptorModel` class ctor.

        :param str country: **Required**. 
            Address country `ISO code <https://developer.visa.com/request_response_codes#isoCodes>`_. 3 characters 
            string.
        :param str county: **Optional**. Address county code. 3 characters string.
        :param str zipCode: **Conditional**. Address ZIP code. 5-9 characters string.
        :param str state: **Condtional**. Address state code. 2 characters string.
        :param str city: **Conditional**. Agent city name. Max 13 characters string. 
        """
        ATTRS = [
            'country',
            'zipCode',
            'state',
            'county',
            'city'
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)


class OriginalDataElementsModel(object):
    """Object model for Original Data Elements object, used for reverse transactions.

    https://en.wikipedia.org/wiki/ISO_8583#Data_elements

    :param int systemsTraceAuditNumber: **Required**. Systems trace audit number, 6 digits integer.
    :param int approvalCode: **Required**. Original AFT acquiring BIN value. 6-11 digits integer.
    :param str transmissionDateTime: **Required**. Original AFT Datetime YYYY-MM-DDThh:mm:ss
    :param str acquiringBin: **Optional**. Approval code from original AFT, 6 characters string.
    """
    ATTRS = [
        'systemsTraceAuditNumber',
        'approvalCode',
        'transmissionDateTime',
        'acquiringBin'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)


class PointOfServiceDataModel(object):
    """Object model for PointOfServiceDataModel data object.

    Optional data structure, included in VisaDirect transactions.

    :param int panEntryMode: **Optional**. Required for Card Present scenarios. 1 digit integer.
    :param int posConditionCode: **Optional**. Required for Card Present scenarios. 2 digits integer.
    :param str motoECIIndicator: **Optional**. If posConditionCode is 59, motoECIIndicator must be between 5-8.
        Default is set to 5 if not provided. If posConditionCode is 0, motoECIIndicator will not be sent. 1 character
        string.
    """
    ATTRS = [
        'panEntryMode',
        'posConditionCode',
        'motoECIIndicator'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)


class PointOfServiceCapabilityModel(object):
    """Object model for PointOfServiceCapabilityModel data object.

    Optional data structure, included in VisaDirect transactions.

    :param int posTerminalType: **Optional**. For Card Present scenarios valid values are 0,3,4. For CNP - 5. 
        1 digit integer.
    :param int posTerminalEntryCapability: **Optional**. For CP valid values are 0,2,9. For CNP - 5. 1 digit integer.
    """
    ATTRS = [
        'posTerminalType',
        'posTerminalEntryCapability',
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)


class MerchantVerificationValueModel(object):
    """Object model for MerchantVerificationValueModel data object.

    Optional data structure, included in VisaDirect transactions.

    :param str mvvVisaAssigned: Visa assigned MVV value. 6 characters hexbin string.
    :param str mvvAcquirerAssigned: Visa assists the acquirer in assigning the last four. 4 characters hexbin string.
    """
    ATTRS = [
        'mvvAcquirerAssigned',
        'mvvVisaAssigned'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)
