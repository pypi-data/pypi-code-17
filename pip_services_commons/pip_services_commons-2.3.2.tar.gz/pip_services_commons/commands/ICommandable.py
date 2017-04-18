# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.ICommandable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for commandable components
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICommandable:
    """
    Interface for components that support command sets
    """

    def get_command_set(self):
        """
        Gets command set for the component

        Returns: component command set
        """
        raise NotImplementedError('Method from interface definition')
