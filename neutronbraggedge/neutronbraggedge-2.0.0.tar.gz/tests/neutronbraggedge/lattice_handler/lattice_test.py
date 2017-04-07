import unittest
import numpy as np
import os
import math
from neutronbraggedge.lattice_handler.lattice import Lattice


class TestLattice(unittest.TestCase):

    def setUp(self):
        pass

    def test_lattice_error_when_bad_structure_given(self):
        """Assert in Lattice - Value Error is raised when bad structure given"""
        _crystal_structure = 'FakeStructure'
        self.assertRaises(ValueError, Lattice, None, _crystal_structure)

    def test_correctly_hkl_returned_for_Si_3entries(self):
        """Assert in Lattice - hkl array correctly calculated and reported for 3 entries"""
        _material = 'Si'
        _crystal_structure = 'FCC'
        _bragg_edge_array = np.array([1, 2, 3])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        _hkl_expected = [[1, 1, 1], [2, 0, 0], [2, 2, 0]]
        self.assertTrue(o_lattice.hkl == _hkl_expected)
    
    #def test_bragg_edge_correctly_formated_with_none_value(self):
        #"""Assert in Lattice - bragg edge array correctly formated with None values"""
        #_material = 'Si'
        #_crystal_structure = 'FCC'
        #_bragg_edge_array = np.array([1, None, 3])
        #o_lattice = Lattice(material = _material,
                            #crystal_structure = _crystal_structure,
                            #bragg_edge_array = _bragg_edge_array)
        #_bragg_edge_array_expected = [1, np.NAN, 3]
        #self.assertEqual(_bragg_edge_array_expected, o_lattice.bragg_edge_array)


    def test_correctly_hkl_returned_for_Si_4entries_with_None(self):
        """Assert in Lattice - hkl array correctly calculated and reported for 4 entries with None"""
        _material = 'Si'
        _crystal_structure = 'FCC'
        _bragg_edge_array = np.array([1, 2, None, 3])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        _hkl_expected = [[1, 1, 1], [2, 0, 0], [2, 2, 0], [2, 2, 2]]
        self.assertTrue(o_lattice.hkl == _hkl_expected)
        
    def test_bragg_edge_crystal_structure_correctly_created(self):
        """Assert in Lattice - bragg edge crystal structure correctly created"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()

        _expected_first_key = [1, 1, 1]
        _expected_first_value = 1.1
        self.assertEqual(_expected_first_key, o_lattice.hkl_bragg_edge[0][0])
        self.assertEqual(_expected_first_value, o_lattice.hkl_bragg_edge[0][1])
        
        _expected_second_key = [2, 0, 0]
        _expected_second_value = 2.2
        self.assertEqual(_expected_second_key, o_lattice.hkl_bragg_edge[1][0])
        self.assertEqual(_expected_second_value, o_lattice.hkl_bragg_edge[1][1])

    def test_bragg_edge_crystal_structure_correctly_created_for_incomplete_list(self):
        """Assert in Lattice - bragg edge crystal structure correctly created for incomplete list"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, None, None, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()

        _expected_first_key = [1, 1, 1]
        _expected_first_value = 1.1
        self.assertEqual(_expected_first_key, o_lattice.hkl_bragg_edge[0][0])
        self.assertEqual(_expected_first_value, o_lattice.hkl_bragg_edge[0][1])
        
        _expected_second_key = [2, 0, 0]
        _expected_second_value = np.NaN
        self.assertEqual(_expected_second_key, o_lattice.hkl_bragg_edge[1][0])
        self.assertTrue(math.isnan(o_lattice.hkl_bragg_edge[1][1]))

    def test_hkl_bragg_edge_correctly_displayed(self):
        """Assert in Lattice - hkl bragg edge correctly displayed"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        self.assertTrue(o_lattice.display_hkl_bragg_edge())
        
    def test_lattice_coefficient_correctly_calculated(self):
        """Assert in Lattice - lattice coefficient correctly calculated for [1,1,1]"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        self.assertEqual(len(_bragg_edge_array), len(o_lattice.lattice_array))
        self.assertAlmostEqual(0.952628, o_lattice.lattice_array[0], delta=0.00001)

    def test_lattice_statistics(self):
        """Assert in Lattice - lattice statistics correctly calculated for Si"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        o_lattice._calculate_lattice_statistics()
        _statistics = o_lattice.lattice_statistics
        
        _delta = 1e-4
        self.assertAlmostEqual(2.549745, _statistics['std'], delta = _delta)
        self.assertAlmostEqual(0.952628, _statistics['min'], delta = _delta)
        self.assertAlmostEqual(7.621024, _statistics['max'], delta = _delta)
        self.assertAlmostEqual(3.433452, _statistics['median'], delta = _delta)
        self.assertAlmostEqual(3.860139, _statistics['mean'][0], delta = _delta)

    def test_display_statistics(self):
        """Assert in Lattice - lattice statistics correctly displayed for Si"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        o_lattice._calculate_lattice_statistics()
        o_lattice.display_lattice_statistics()

    def test_display_recap(self):
        """Assert in Lattice - lattice recap displayed correctly"""
        _material = "Si"
        _crystal_structure = "FCC"
        _bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material = _material,
                            crystal_structure = _crystal_structure,
                            bragg_edge_array = _bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        o_lattice._calculate_lattice_statistics()
        o_lattice.display_recap()
        
if __name__ == '__main__':
    unittest.main()
