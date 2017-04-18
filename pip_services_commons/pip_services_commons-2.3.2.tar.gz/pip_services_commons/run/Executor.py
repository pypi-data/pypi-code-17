# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.Executor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Executor component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IExecutable import IExecutable
from .IParamExecutable import IParamExecutable
from .Parameters import Parameters

class Executor:
    """
    Helper class that triggers execution for components
    """

    @staticmethod
    def execute_one(correlation_id, component, args):
        """
        Triggers execution for components that implement IExecutable interfaces

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components:  components a list of components to be notified
            args: a set of parameters to pass to executed components

        Returns: execution results
        """
        if isinstance(component, IExecutable):
            return component.execute(correlation_id, parameters)

        return None

    @staticmethod
    def execute(correlation_id, components, args = None):
        """
        Triggers execution for components that implement IExecutable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components:  components a list of components to be notified
            args: a set of parameters to pass to executed components

        Returns: array of execution results
        """
        results = []

        if components == None:
            return

        args = args if args != None else Parameters()
        for component in components:
            result = Executor.execute_one(correlation_id, component, args)
            results.append(result)

        return results
