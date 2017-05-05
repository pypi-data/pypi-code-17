from digitrecklib.Config import *
from digitrecklib.core.Constants import *
from digitrecklib.core.HTTPInterface import *

class IRequester(object):
    """docstring for IRequester"""

    '''
    * Gets Config Info
    *
    * Initialize Http Interface Module
    '''
    def __init__(self, configInfo):
        self.httpInterface = HTTPInterface(configInfo[Config.SERVER_KEY], configInfo[Config.PRIVATE_KEY], BASE_URL)
        
    def request(self,req, array_data, subURL):
        res = self.httpInterface.send(req, array_data, subURL)
        return res

