# -*- coding: utf-8 -*-
"""
    pip_services_net.messaging.MessageEnvelop
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Message envelop implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.convert import StringConverter
from pip_services_commons.data import IdGenerator

class MessageEnvelop(object):
    reference = None
    message_id = None
    message_type = None
    correlation_id = None
    message = None
    reference = None

    def __init__(self, correlation_id = None, message_type = None, message = None):
        self.correlation_id = correlation_id
        self.message_type = message_type
        self.message = message
        self.message_id = IdGenerator.next_long()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['reference']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        output = "[" 
        output += self.correlation_id if self.correlation_id != None else "---"
        output += "," 
        output += self.message_type if self.message_type != None else "---" 
        output += ","
        output += StringConverter.to_string(self.message) if self.message != None else "--"
        output += "]"
        return output
