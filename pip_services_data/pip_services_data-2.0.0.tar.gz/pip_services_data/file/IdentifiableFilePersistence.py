# -*- coding: utf-8 -*-
"""
    pip_services_data.file.IdentifiableFilePersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Identifiable file persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..memory.IdentifiableMemoryPersistence import IdentifiableMemoryPersistence
from .JsonFilePersister import JsonFilePersister

class IdentifiableFilePersistence(IdentifiableMemoryPersistence):
    _persister = None

    def __init__(self, persister):
        super(FilePersistence, self).__init__()

        self._persister = persister if persister != None else JsonFilePersister()
        self._saver = self._persister
        self._loader = self._persister

    def configure(self, config):
        self._persister.configure(config)
