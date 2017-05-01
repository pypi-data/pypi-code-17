from Constants import *
from HTTPInterface import *

import imp

class Helper(object):
    """docstring for Helper"""

    def __init__(self, configInfo):
        configInfo[BASE_URL] = PROD_URL
        self.httpInterface = HTTPInterface(configInfo[SERVER_KEY], configInfo[PRIVATE_KEY],
                                           configInfo[BASE_URL])


    @staticmethod
    def checkDependency(module):
        try:
            imp.find_module(module)
            return True
        except ImportError:
            return False

    # checks required module dependencies...
    def checkDependencies(self):
        if not self.checkDependency('requests'):
            Logger.logInfo("requests module not found")
            return False

