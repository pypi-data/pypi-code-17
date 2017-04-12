# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.FileConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    File config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams
from .ConfigReader import ConfigReader

class FileConfigReader(ConfigReader):
    _path = None

    def __init__(self, path = None):
        super(FileConfigReader, self).__init__()
        self._path = path
        
    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def configure(self, config):
        super(FileConfigReader, self).configure(config)
        this._path = config.get_as_string_with_default("path", self._path)
