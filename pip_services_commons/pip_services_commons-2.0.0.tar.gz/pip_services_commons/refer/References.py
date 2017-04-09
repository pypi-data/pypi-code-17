# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.References
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Referencescomponent implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading

from .IReferenceable import IReferenceable
from .IUnreferenceable import IUnreferenceable
from .IReferences import IReferences
from .Reference import Reference
from .ReferenceQuery import ReferenceQuery
from .ReferenceException import ReferenceException

class References(object, IReferences):
    """
    Basic implementation of IReferences that stores component as a flat list
    """

    _references = None
    _lock = None

    def __init__(self, tuples = None):
        self._references = []
        self._lock = threading.Lock()

        if tuples != None:
            index = 0
            while index < len(tuples):
                if index + 1 >= len(tuples):
                    break
                self.put(tuples[index], tuples[index + 1])
                index = index + 2


    def put(self, locator, component):
        if component == None:
            raise Exception("Component cannot be null")

        self._lock.acquire()
        try:
            self._references.append(Reference(locator, component))
        finally:
            self._lock.release()


    def remove(self, locator):
        if locator == None:
            return None

        self._lock.acquire()
        try:
            for reference in reversed(self._references):
                if reference.match(locator):
                    self._references.remove(reference);
                    return reference.get_component()
        finally:
            self._lock.release()
        
        return None

    def remove_all(self, locator):
        components = []

        if locator == None:
            return components

        self._lock.acquire()
        try:
            for reference in reversed(self._references):
                if reference.match(locator):
                    self._references.remove(reference);
                    components.append(reference.get_component())
        finally:
            self._lock.release()
        
        return components


    def get_all(self):
        components = []
        
        self._lock.acquire()
        try:
            for reference in self._references:
                components.append(reference.get_component())
        finally:
            self._lock.release()

        return components


    def get_optional(self, locator):
        try:
            return self.find(ReferenceQuery(locator), False)
        except Exception as ex:
            return []


    def get_required(self, locator):
        return self.find(ReferenceQuery(locator), True)


    def get_one_optional(self, locator):
        try:
            components = self.find(ReferenceQuery(locator), False)
            return components[0] if len(components) > 0 else None
        except Exception as ex:
            return None


    def get_one_required(self, locator):
        components = self.find(ReferenceQuery(locator), True)
        return components[0] if len(components) > 0 else None


    def find(self, query, required):
        if query == None:
            raise Exception("Query cannot be null")

        components = []

        self._lock.acquire()
        try:
            index = 0 if query.ascending else len(self._references) - 1
            
            # Locate the start
            if query.start_locator != None:
                while index >= 0 and index < len(self._references):
                    reference = self._references[index]
                    if reference.match(query.start_locator):
                        break
                    index = index + (1 if query.ascending else -1)

            # Search all references
            while index >= 0 and index < len(self._references):
                reference = self._references[index]
                if reference.match(query.locator):
                    component = reference.get_component()
                    components.append(component)
                index = index + (1 if query.ascending else -1)

            if len(components) == 0 and required:
                raise ReferenceException(None, query.locator)
        finally:
            self._lock.release()

        return components


    @staticmethod
    def from_tuples(*tuples):
        return References(tuples)
