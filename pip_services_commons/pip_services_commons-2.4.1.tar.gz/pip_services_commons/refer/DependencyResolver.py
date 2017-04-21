# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.DependencyResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Dependency resolver component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IReferenceable import IReferenceable
from ..config.IReconfigurable import IReconfigurable
from ..convert.StringConverter import StringConverter
from ..refer.Descriptor import Descriptor
from ..refer.ReferenceException import ReferenceException

class DependencyResolver(object, IReconfigurable, IReferenceable):
    _dependencies = None
    _references = None

    def __init__(self, config = None, references = None):
        self._dependencies = {}
        if config != None:
            self.configure(config)
        if references != None:
            self.set_references(references)


    def configure(self, config):
        dependencies = config.get_section("dependencies")
        names = dependencies.get_key_names()
        for name in names:
            locator = dependencies.get(name)
            if locator == None:
                continue
            
            try:
                descriptor = Descriptor.from_string(locator)
                if descriptor != None:
                    self._dependencies[name] = descriptor
                else:
                    self._dependencies[name] = locator
            except Exception as ex:
                self._dependencies[name] = locator


    def set_references(self, references):
        self._references = references


    def put(self, name, locator):
        self._dependencies[name] = locator


    def _locate(self, name):
        if name == None:
            raise Exception("Dependency name cannot be null")
        if self._references == None:
            raise Exception("References shall be set")
        
        return self._dependencies[name] if self._dependencies.has_key(name) else None


    def get_optional(self, name):
        locator = self._locate(name)
        return self._references.get_optional(locator) if locator != None else None


    def get_required(self, name):
        locator = self._locate(name)
        if locator == None:
            raise ReferenceException(None, name)
        
        return self._references.get_required(locator)


    def get_one_optional(self, name):
        locator = self._locate(name)
        return self._references.get_one_optional(locator) if locator != None else None


    def get_one_required(self, name):
        locator = self._locate(name)
        if locator == None:
            raise ReferenceException(None, name)
        
        return self._references.get_one_required(locator)


    def find(self, name, required):
        if name == None:
            raise Exception("Name cannot be null")
        
        locator = self._locate(name)
        if locator == None:
            if required:
                raise ReferenceException(None, name)
            return None
        
        return self._references.find(locator, required)


    @staticmethod
    def from_tuples(*tuples):
        result = DependencyResolver()
        if tuples == None or len(tuples) == 0:
            return result
        
        index = 0
        while index < len(tuples):
            if index + 1 >= len(tuples):
                break

            name = StringConverter.to_string(tuples[index])
            locator = tuples[index + 1]

            result.put(name, locator)
            index = index + 2
        
        return result
