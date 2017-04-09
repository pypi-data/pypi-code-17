# -*- coding: utf-8 -*-
"""
    tests.mongodb.test_DummyMongoDbPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import pytest

from pip_services_commons.config import YamlConfigReader
from .DummyMongoDbPersistence import DummyMongoDbPersistence
from ..DummyPersistenceFixture import DummyPersistenceFixture

config = YamlConfigReader.read_config(None, './config/test_connections.yaml')
db_config = config.get_section('mongodb')

test_enabled = False

#@pytest.mark.skipif(not test_enabled, reason='MongoDB persistence is not configured')
class TestDummyMongoDbPersistence:

    persistence = None
    fixture = None

    @classmethod
    def setup_class(cls):
        cls.persistence = DummyMongoDbPersistence()
        cls.fixture = DummyPersistenceFixture(cls.persistence)

        cls.persistence.configure(db_config)
        cls.persistence.open(None)

    @classmethod
    def teardown_class(cls):
        cls.persistence.close(None)

    def setup_method(self, method):
        self.persistence.clear(None)
    
    def test_crud_operations(self):
        self.fixture.test_crud_operations()
