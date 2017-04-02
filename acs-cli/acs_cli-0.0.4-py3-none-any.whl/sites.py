from .common import APIBase


class Sites(APIBase):
    def __init__(self, base_url):
        APIBase.__init__(self, base_url, 'alfresco', 'sites')
