# -*- coding: utf-8 -*-
"""
    pip_services_logging.services.version1.LoggingHttpServiceV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging HTTP service implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.refer import Descriptor
from pip_services_net.rest import CommandableHttpService

class LoggingHttpServiceV1(CommandableHttpService):
    
    def __init__(self):
        super(LoggingHttpServiceV1, self).__init__('logging')
        self._dependency_resolver.put('controller', Descriptor('pip-services-logging', 'controller', '*', '*', '*'))
