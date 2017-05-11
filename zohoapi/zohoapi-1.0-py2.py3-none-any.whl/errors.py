class ZohoGeneralError(Exception):
    """
    A non-specific Zoho error.
    """
    message = u'Error Code {url}. Response content: {content}'

    def __init__(self, url, content):
        self.url = url
        self.content = content

    def __str__(self):
        return self.message.format(url=self.url, content=self.content)

    def __unicode__(self):
        return self.__str__()


class ZohoConnectionError(ZohoGeneralError):
    message = u'Error Connecting to Zoho API. {content}: {url}'


class ZohoBadRecordError(ZohoGeneralError):
    message = u'Record Unavailable {url}. {content}'


class ZohoNoDataError(ZohoGeneralError):
    message = u'No Data {url}. {content}'
