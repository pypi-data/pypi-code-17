from .common import APIBase


class People(APIBase):
    def __init__(self, base_url):
        # alfresco = 'core' API
        APIBase.__init__(self, base_url, 'alfresco', 'people')

