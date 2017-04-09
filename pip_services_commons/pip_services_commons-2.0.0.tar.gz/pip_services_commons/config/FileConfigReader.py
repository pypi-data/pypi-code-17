# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.FileConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    File config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams
from .CachedConfigReader import CachedConfigReader
from .IConfigurable import IConfigurable

class FileConfigReader(CachedConfigReader, IConfigurable):
    _path = None

    def __init__(self, path = None):
        self._path = path
        
    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def configure(self, config):
        this._path = config.get_as_string_with_default("path", self._path)
