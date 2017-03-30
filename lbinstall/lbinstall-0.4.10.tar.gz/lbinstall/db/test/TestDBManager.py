###############################################################################
# (c) Copyright 2016 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''

Tests for the local DBManager.

@author: lben
'''
import unittest

from lbinstall.db.DBManager import DBManager
from lbinstall.db.ChainedDBManager import ChainedConfigManager
import os
import shutil


class Test(unittest.TestCase):

    def setUp(self):

        # create siteroot - Needed by the Chained DB
        if os.environ.get('MYSITEROOT', None):
            self.siteroot = os.environ['MYSITEROOT']
        else:
            self.siteroot = "/tmp/siteroot"
        shutil.rmtree(self.siteroot, ignore_errors=True)
        os.mkdir(self.siteroot)
        os.mkdir(os.path.join(self.siteroot, 'etc'))
        self._chained_db = ChainedConfigManager(self.siteroot)
        self.db = DBManager(':memory:', 'var/lib/db/packages.db',
                            self._chained_db)

    def tearDown(self):
        shutil.rmtree(self.siteroot, ignore_errors=True)
        pass

    def testAddPackage(self):

        from lbinstall.DependencyManager import Package as dmPackage
        from lbinstall.DependencyManager import Provides as dmProvides
        from lbinstall.DependencyManager import Requires as dmRequires

        provides = [dmProvides("P1", "1.0.0", "1"),
                    dmProvides("P", None, None)]
        requires = [dmRequires("P0", "4.2.0", "1")]
        p1 = dmPackage("P1", "1.0.0", "1", group="LHCb")
        for t in provides:
            p1.provides.append(t)
        for t in requires:
            p1.requires.append(t)
        self.db.addPackage(p1, None)

        p2 = dmPackage("P2", "1.0.0", "1", group="LHCb")
        for t in [dmProvides("P2", "1.0.0", "1"), dmProvides("P", None, None)]:
            p2.provides.append(t)

        for t in [dmRequires("P1", "1.0.0", "1")]:
            p2.requires.append(t)
        self.db.addPackage(p2, None)

        test = self.db.findProvidesByName("P")
        self.assertEquals(len(list(test)), 2,
                          "Make sure two packages provide P")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInsert']
    unittest.main()
