import unittest
import os
from neutronbraggedge import config
from neutronbraggedge.material_handler.retrieve_metadata_table import RetrieveMetadataTable


class TestRetrieveMetadataTable(unittest.TestCase):

    def setUp(self):
        _config_file = config.config_file
        self._config_file = os.path.abspath(_config_file)

    def test_retrieve_table_from_url(self):
        """checking if the table is correctly loaded from URL"""
       
        retrieve_meta = RetrieveMetadataTable(use_local_table=False)
        _table = retrieve_meta.get_table()
        _shape = _table.shape

        nbr_column = 3
        self.assertEqual(_shape[1], nbr_column)
        
        value_0_0 = 'Diamond (FCC)'
        self.assertEqual(value_0_0, _table.values[0][1])

    def test_retrieve_local_table(self):
        """checking if the local table is correctly loaded"""
        
        retrieve_meta = RetrieveMetadataTable()
        _table = retrieve_meta.get_table()
        _shape = _table.shape
        
        nbr_column = 3
        self.assertEqual(_shape[1], nbr_column)
        
        value_0_0 = 'Diamond (FCC)'
        self.assertEqual(value_0_0, _table.values[0][1])


if __name__ == '__main__':
    unittest.main()
