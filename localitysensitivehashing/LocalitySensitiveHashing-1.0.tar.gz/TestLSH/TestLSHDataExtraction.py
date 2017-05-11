import LocalitySensitiveHashing
import unittest

class TestLSHDataExtraction(unittest.TestCase):

    def setUp(self):
        self.lsh = LocalitySensitiveHashing.LocalitySensitiveHashing( 
                 datafile = "data_for_lsh.csv",  dim = 10, r = 50, b = 100)
        self.lsh.get_data_from_csv()
        self.data_dict = self.lsh._data_dict

    def test_successful_data_extraction(self):
        print("testing data extraction from CSV")
        self.assertEqual( len(self.data_dict), 80 )
        self.assertEqual( 'sample0_0' in self.data_dict, True )

def getTestSuites(type):
    return unittest.TestSuite([
            unittest.makeSuite(TestLSHDataExtraction, type)
                             ])                    

if __name__ == '__main__':
    unittest.main()

