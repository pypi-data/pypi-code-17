# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.IReferences
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for references components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IReferences:
    """
    Set of component references with abilities to add new references, find reference using locators
    or remove reference from the set
    """

    def put(self, reference, locator = None):
        """
        Puts a new component reference to the set with optional locator

        Args:
            locator: a locator to find the reference
            reference: a component reference to be added
        """
        raise NotImplementedError('Method from interface definition')

    def remove(self, locator):
        """
        Removes component reference from the set.
        The method removes only the last reference.

        Args:
            locator: a locator to find the reference to remove

        Returns: a removed reference
        """
        raise NotImplementedError('Method from interface definition')
        
    def get_all(self):
        """
        Gets all stored component references

        Returns: a list with component references
        """
        raise NotImplementedError('Method from interface definition')

    def get_optional(self, locator):
        """
        Gets a list of component references that match provided locator

        Args:
            locator: a locator to find references

        Returns: a list with found component references
        """
        raise NotImplementedError('Method from interface definition')

    def get_required(self, locator):
        """
        Gets a list of component references that match provided locator.
        If no references found an exception is thrown

        Args:
            locator: a locator to find references

        Returns: a list with found component references
        Raises: ReferenceException when no single component reference is found 
        """
        raise NotImplementedError('Method from interface definition')

    def get_one_optional(self, locator):
        """
        Gets a component references that matches provided locator.
        The search is performed from latest added references.

        Args:
            locator: a locator to find a reference

        Returns: a found component reference or None if nothing was found
        """
        raise NotImplementedError('Method from interface definition')

    def get_one_required(self, locator):
        """
        Gets a component references that matches provided locator.
        The search is performed from latest added references.

        Args:
            locator: a locator to find a reference

        Returns: a found component reference
        Raises: ReferenceException when requested component wasn't found
        """
        raise NotImplementedError('Method from interface definition')

    def get_one_before(self, reference, locator):
        """
        Gets a component references that matches provided locator.

        Args:
            reference: a component reference to start the search and continue form latest to oldest
            locator: a locator to find a reference

        Returns: a found component reference
        Raises: ReferenceException when requested component wasn't found
        """
        raise NotImplementedError('Method from interface definition')
