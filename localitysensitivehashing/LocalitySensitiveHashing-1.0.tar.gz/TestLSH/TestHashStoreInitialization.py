import LocalitySensitiveHashing
import unittest

class TestHashStoreInitialization(unittest.TestCase):

    def setUp(self):
        self.lsh = LocalitySensitiveHashing.LocalitySensitiveHashing( 
                  datafile = "data_for_lsh.csv",  dim = 10, r = 50, b = 100)
        self.lsh.get_data_from_csv()
        self.lsh.initialize_hash_store()

    def test_successful_hash_store_initialization(self):
        print("testing hash store initialization")
        self.assertEqual( len(self.lsh.hash_store), 5000)

def getTestSuites(type):
    return unittest.TestSuite([
            unittest.makeSuite(TestHashStoreInitialization, type)
                             ])                    

if __name__ == '__main__':
    unittest.main()
