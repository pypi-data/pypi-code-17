# -*- coding: utf-8 -*-
"""
    pip_services_logging.container.LoggingProcess
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging process container implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_container.ProcessContainer import ProcessContainer
from ..build.LoggingFactory import LoggingFactory, LoggingFactoryDescriptor

class LoggingProcess(ProcessContainer):

    def _init_references(self, references):
        super(LoggingProcess, self)._init_references(references)
        
        # Factory to statically resolve logging components
        references.put(LoggingFactoryDescriptor, LoggingFactory())

    def run_with_args(self):
        self.run_with_config_from_args_or_file('logging', "./config/config.yaml")
