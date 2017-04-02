#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.
from PyQt5 import QtGui

# Local modules.
import pyqttango #@UnusedImport

# Globals and constants variables.

class Test(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.app = QtGui.QGuiApplication([])

    def testhasThemeIcon(self):
        self.assertEqual('tango', QtGui.QIcon.themeName())
        self.assertTrue(QtGui.QIcon.hasThemeIcon("accessories-calculator"))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
