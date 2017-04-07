import unittest
import os
from neutronbraggedge.material_handler.retrieve_material_metadata import RetrieveMaterialMetadata


class TestRetrieveMaterialMetadata(unittest.TestCase):

    def setUp(self):
        pass

    def test_retrieve_lattice_of_si_via_web(self):
        """Assert in RetrieveMaterialMetadata - value of lattice retrieved from Si via web table"""
        retrieve_material = RetrieveMaterialMetadata(material = 'Si',
                                                     use_local_table = False)
        lattice_expected = 5.431
        self.assertAlmostEqual(lattice_expected, retrieve_material.lattice, delta=0.001)

    def test_retrieve_lattice_of_si_via_local_table(self):
        """Assert in RetrieveMaterialMetadata - value of lattice retrieved from Si via local table"""
        retrieve_material = RetrieveMaterialMetadata(material = 'Si',
                                                     use_local_table = True)
        lattice_expected = 5.431591 #higher precision on local table
        self.assertEqual(lattice_expected, retrieve_material.lattice)

    def test_raise_NameError_no_arguments(self):
        """Assert in RetrieveMaterialMetadata - NameError is raised when no arguments is given"""
        self.assertRaises(NameError, RetrieveMaterialMetadata)
        
    def test_raise_NameError_material_unknown(self):
        """Assert in RetrieveMaterialMetadata - NameError is raised if material is unknown"""
        self.assertRaises(KeyError, RetrieveMaterialMetadata, 'unknown')

    def test_retrieving_full_list_of_material(self):
        """Assert in RetrieveMaterialMetadata - Full list of material available returned"""
        retrieve_material = RetrieveMaterialMetadata(material = 'all',
                                                     use_local_table = False)
        
        list_returned = retrieve_material.full_list_material()
        list_expected_3_first = ['C (diamond)', 'Si', 'Ge']
        self.assertTrue(all(list_returned[0:3] == list_expected_3_first))
        

if __name__ == '__main__':
    unittest.main()
