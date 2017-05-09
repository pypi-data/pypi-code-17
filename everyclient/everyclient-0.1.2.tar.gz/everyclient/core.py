# -*- coding: utf-8 -*-
from .apimixin import APIMixin

class EveryClient(APIMixin): 
    '''Inherit from APIMixin

    Default Settings:
        retries = 5
        redirects = 2
        timeout = 120
        read = None
        domain = 'https://api.every-sense.com'
        port = 8001
        headers = {'Content-Type': 'application/json;charset=utf-8'}

    '''
    pass
