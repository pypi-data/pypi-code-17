# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.ConfigParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Config params implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..data.StringValueMap import StringValueMap
from ..reflect.RecursiveObjectReader import RecursiveObjectReader

class ConfigParams(StringValueMap):
    """
    Map with configuration parameters that use complex keys with dot notation and simple string values.

    Example of values, stored in the configuration parameters:
    - Section-1.Subsection-1-1.Key-1-1-1=123
    - Section-1.Subsection-1-2.Key-1-2-1="ABC"
    - Section-2.Subsection-1.Key-2-1-1="2016-09-16T00:00:00.00Z"

    Configuration parameters support getting and adding sections from the map.

    Also, configuration parameters may come in a form of parameterized string:
    Key1=123;Key2=ABC;Key3=2016-09-16T00:00:00.00Z

    All keys stored in the map are case-insensitive.
    """

    def __init__(self, values = None):
        super(ConfigParams, self).__init__(values)

    def get_section_names(self):
        sections = []
        
        for (key, value) in self.items():
            pos = key.find('.')
            if pos > 0:
                key = key[0 : pos]

            # Perform case sensitive search
            found = False
            for section in sections:
                if section.lower() == key.lower():
                    found = True
                    break
                
            if not found:
                sections.append(key)
        
        return sections


    def get_section(self, section):
        result = ConfigParams()
        prefix = section + "."
        
        for (key, value) in self.items():
            # Prevents exception on the next line
            if len(key) < len(prefix):
                continue
            
            # Perform case sensitive match
            key_prefix = key[: len(prefix)]
            if key_prefix.lower() == prefix.lower():
                key = key[len(prefix): ]
                result[key] = value
        
        return result


    def _is_shadow_name(self, name):
        return name == None or len(name) == 0 or name[0] == "#" or name[0] == "!"


    def add_section(self, section, section_params):
        if section == None:
            raise Exception("Section name cannot be null")

        section = "" if self._is_shadow_name(section) else section 
        
        if section_params == None or len(section_params) == 0:
            return

        for (key, value) in section_params.items():
            key = "" if self._is_shadow_name(key) else key
            
            if len(key) > 0 and len(section) > 0:
                key = section + "." + key
            elif len(key) == 0:
                key = section

            self[key] = value


    def override(self, config_params):
        map = StringValueMap.from_maps(self, config_params)
        return ConfigParams(map)


    def set_defaults(self, default_config_params):
        map = StringValueMap.from_maps(default_config_params, self)
        return ConfigParams(map);


    @staticmethod
    def from_value(value):
        map = RecursiveObjectReader.get_properties(value)
        return ConfigParams(map)

    
    @staticmethod
    def from_tuples(*tuples):
        map = StringValueMap.from_tuples_array(tuples)
        return ConfigParams(map)

    
    @staticmethod
    def from_string(line):
        map = StringValueMap.from_string(line)
        return ConfigParams(map)


    @staticmethod
    def merge_configs(*configs):
        map = StringValueMap.from_maps(*configs)
        return ConfigParams(map)
