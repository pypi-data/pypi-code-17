# -*- coding: utf-8 -*-
"""
    pip_services_runtime.refer.Descriptor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component descriptor implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.ConfigException import ConfigException

class Descriptor(object):
    """
    Component descriptor used to find a component by its descriptive elements:
    - logical group: package or other logical group of components like 'pip-services-storage-blocks'
    - component type: identifies component interface like 'controller', 'services' or 'cache'
    - component kind: identifies component implementation like 'memory', 'file' or 'mongodb', ...
    - component name: identifies component internal content, ...
    - implementation version: '1.0', '1.5' or '10.4'
    """

    _group = None
    _type = None
    _kind = None
    _name = None
    _version = None
    
    def __init__(self, group, tipe, kind, name, version):
        """
        Creates instance of a component descriptor

        Args:
            group: logical group: 'pip-services-runtime', 'pip-services-logging'
            type: external type: 'cache', 'services' or 'controllers'
            kind - implementation: 'memory', 'file' or 'memcached' 
            name - internal content
            version: compatibility version: '1.0'. '1.5' or '10.4'
        """
        group = None if "*" == group else group 
        tipe = None if "*" == tipe else tipe
        kind = None if "*" == kind else kind
        name  = None if "*" == name else name
        version = None if "*" == version else version
        
        self._group = group
        self._type = tipe
        self._kind = kind
        self._name = name
        self._version = version

    def get_group(self): 
        """
        Gets the component group
        Returns: the component group
        """
        return self._group 

    def get_type(self):
        """
        Gets the component type
        Returns: the component type
        """ 
        return self._type

    def get_kind(self):
        """
        Gets the component kind
        Returns: the component kind
        """
        return self._kind

    def get_name(self):
        """
        Gets the component name
        Returns: the component name
        """ 
        return self._name 

    def get_version(self):
        """
        Gets the implementation version
        Returns: the implementation version
        """ 
        return self._version 

    def _match_field(self, field1, field2):
        return field1 == None \
            or field2 == None \
            or field1 == field2

    def match(self, descriptor):
        """
        Matches this descriptor to another descriptor.
        All '*' or null descriptor elements match to any other value.
        Specific values must match exactly.
         
        Args:
            descriptor: another descriptor to match this one.

        Returns: True if descriptors match or False otherwise. 
        """
        return self._match_field(self._group, descriptor.get_group()) \
            and self._match_field(self._type, descriptor.get_type()) \
            and self._match_field(self._kind, descriptor.get_kind()) \
            and self._match_field(self._name, descriptor.get_name()) \
            and self._match_field(self._version, descriptor.get_version())

    def _exact_match_field(self, field1, field2):
        if field1 == None and field2 == None:
            return True
        if field1 == None or field2 == None:
            return False
        return field1 == field2

    def exact_match(self, descriptor):
        """
        Matches this descriptor to another descriptor exactly.
         
        Args:
            descriptor: another descriptor to match this one.

        Returns: True if descriptors match or False otherwise. 
        """
        return self._exact_match_field(self._group, descriptor.get_group()) \
            and self._exact_atch_field(self._type, descriptor.get_type()) \
            and self._exact_match_field(self._kind, descriptor.get_kind()) \
            and self._exact_match_field(self._name, descriptor.get_name()) \
            and self._exact_match_field(self._version, descriptor.get_version())

    def is_complete(self):
        return self._group != None and self._type != None \
            and self._kind != None and self._name != None and self._version != None

    def __eq__(self, other):
        if isinstance(other, Descriptor):
            return self.match(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        result = ''
        result += self._group if self._group != None else '*'
        result += ':'
        result += self._type if self._type != None else '*'
        result += ':'
        result += self._kind if self._kind != None else '*'
        result += ':'
        result += self._name if self._name != None else '*'
        result += ':'
        result += self._version if self._version != None else '*'
        return result
    
    @staticmethod
    def from_string(value):
        if value == None or len(value) == 0:
            return None
                
        tokens = value.split(":")
        if len(tokens) != 5:
            raise ConfigException(
                None, "BAD_DESCRIPTOR", "Descriptor " + str(value) + " is in wrong format"
            ).with_details("descriptor", value)
            
        return Descriptor(tokens[0].strip(), tokens[1].strip(), tokens[2].strip(), tokens[3].strip(), tokens[4].strip())

