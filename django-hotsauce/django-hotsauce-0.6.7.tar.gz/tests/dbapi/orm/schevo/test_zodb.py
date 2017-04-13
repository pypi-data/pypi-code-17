#!/usr/bin/env python
#from schevo.database2 import Database
from schevo.database import format_dbclass, equivalent
from test_support import unittest
from notmm.dbapi.orm import ZODBFileStorageProxy

class ZODBFileProxyTestCase(unittest.TestCase):

    connected = False

    def setUp(self):
        self.dbname = '127.0.0.1:4343'

    def tearDown(self):
        pass

    def test_initdb(self):
        db = ZODBFileStorageProxy(self.dbname)
        #db2 = ZODBFileStorageProxy(self.dbname)
        #self.assertEqual(equivalent(db, db2), True)
        self.assertEqual(db != None, True)
        db.initdb(db.conn)
        print db.extents()
