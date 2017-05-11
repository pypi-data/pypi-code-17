#!/usr/bin/env python

import unittest
import TestHashStoreInitialization
import TestLSHDataExtraction

class LSHTestCase( unittest.TestCase ):
    def checkVersion(self):
        import LSH

testSuites = [unittest.makeSuite(LSHTestCase, 'test')] 

for test_type in [
            TestLSHDataExtraction,
            TestHashStoreInitialization,
    ]:
    testSuites.append(test_type.getTestSuites('test'))


def getTestDirectory():
    try:
        return os.path.abspath(os.path.dirname(__file__))
    except:
        return '.'

import os
os.chdir(getTestDirectory())

runner = unittest.TextTestRunner()
runner.run(unittest.TestSuite(testSuites))
