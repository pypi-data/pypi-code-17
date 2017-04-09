# -*- coding: utf-8 -*-
"""
    pip_services_net.messaging.IMessageReceiver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for message receivers.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IMessageReceiver:

    def receive_message(self, message, queue):
        raise NotImplementedError('Method from interface definition')