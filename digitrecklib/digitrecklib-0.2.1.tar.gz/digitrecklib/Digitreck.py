from digitrecklib.requester.Requester import *

class Digitreck(object):
    """docstring for Digitreck"""

    '''
    * Gets Config Info
    *
    * Initialize Http Interface Module
    '''
    def __init__(self, configInfo):
        self.requester = Requester(configInfo)
    
    
    def getInstance(self):
        return self.requester