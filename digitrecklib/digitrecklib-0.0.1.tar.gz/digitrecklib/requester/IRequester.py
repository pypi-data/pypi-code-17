from digitrecklib.core.Constants import *
from digitrecklib.core.Helper import *

class IRequester(object):
    """docstring for IRequester"""

    '''
    * Gets Config Info
    *
    * Initialize Http Interface Module
    '''
    def __init__(self, configInfo):
        configInfo[BASE_URL] = PROD_URL
        self.httpInterface = HTTPInterface(configInfo[SERVER_KEY], configInfo[PRIVATE_KEY],
                                           configInfo[BASE_URL])
        
    def request(self,req, array_data, subURL):
        res = self.httpInterface.send(req, array_data, subURL)
        return res

