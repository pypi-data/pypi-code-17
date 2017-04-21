from datetime import datetime


class AbstractPaymentAccountAttributesInquiryModel(object):
    """Abstract model for PAAI APIs.
    
    Inherited by concrete models.
    
    Implements generation of RRN and population of systemsTraceAuditNumber (STAN) attribute.
    
    :param int systemsTraceAuditNumber: **Required**. Systems Trace Audit Number (STAN). 6 digits integer.
    :param str retrievalReferenceNumber: **Optional**. Optional Retrieval Reference Number. 12 characters string. 
        If not provided, generated automatically.
    """
    def __init__(self, **kwargs):
        self.systemsTraceAuditNumber = kwargs['systemsTraceAuditNumber']

        try:
            self.retrievalReferenceNumber = kwargs['retrievalReferenceNumber']
        except KeyError:
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
