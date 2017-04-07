import unittest
import os
import numpy as np
from neutronbraggedge.braggedges_handler.braggedge_calculator import BraggEdgeCalculator


class TestBraggEdgesHandler(unittest.TestCase):

    def setUp(self):
        pass

    def test_calling_without_arguments(self):
        """Testing that class can be called with default arguments from python2 and 3"""
        _handler = BraggEdgeCalculator()
        self.assertEqual("FCC", _handler.structure)
        
    def test_braggedge_calculator_eror_when_bad_structure_given(self):
        """Assert in braggedge calculator - error is raised when bad structure given"""
        _structure_name = "FakeStructure"
        self.assertRaises(ValueError, BraggEdgeCalculator, _structure_name)

    def test_right_structure_name_is_passed_in_constructor(self):
        """Assert that structure name passed in constructor is correctly used"""
        _structure_name = "BCC"
        _handler = BraggEdgeCalculator(structure_name = _structure_name)
        self.assertEqual("BCC", _handler.structure)
        
    def test_right_structure_name_is_passed_in_assigned(self):
        """Assert that structure name assigned is correctly saved"""
        _structure_name = "BCC"
        _handler = BraggEdgeCalculator()
        _handler.structure = _structure_name
        self.assertEqual("BCC", _handler.structure)
        
    def test_right_hkl_number_calculated_for_BCC(self):
        """Assert that the right number of hkl sets is returned for BCC"""
        _structure_name = "BCC"
        _handler = BraggEdgeCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual(5, len(_hkl))
        
    def test_right_hkl_number_calculated_for_FCC(self):
        """Assert that the right number of hkl sets is returned for FCC"""
        _structure_name = "FCC"
        _handler = BraggEdgeCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual(5, len(_hkl))

    def test_right_hkl_set_is_calculated_for_FCC(self):
        """Assert that the right set of hkl sets is returned for FCC"""
        _structure_name = "FCC"
        _handler = BraggEdgeCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual([1, 1, 1], _hkl[0])
        self.assertEqual([2, 0, 0], _hkl[1])
        self.assertEqual([2, 2, 0], _hkl[2])
        self.assertEqual([2, 2, 2], _hkl[3])
        self.assertEqual([3, 1, 1], _hkl[4])    
           
    def test_right_hkl_number_calculated_for_BCC(self):
        """Assert that the right number of hkl sets is returned for BCC"""
        _structure_name = "BCC"
        _handler = BraggEdgeCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual(5, len(_hkl))

    def test_right_hkl_set_is_calculated_for_BCC(self):
        """Assert that the right set of hkl sets is returned for BCC"""
        _structure_name = "BCC"
        _handler = BraggEdgeCalculator(structure_name = _structure_name, 
                                             number_of_set = 5)
        _handler.calculate_hkl()
        _hkl = _handler.hkl
        self.assertEqual([1, 1, 0], _hkl[0])
        self.assertEqual([2, 0, 0], _hkl[1])
        self.assertEqual([2, 1, 1], _hkl[2])
        self.assertEqual([2, 2, 0], _hkl[3])
        self.assertEqual([2, 2, 2], _hkl[4])

    def test_calculate_bragg_edges_algorithm_fail_when_no_lattice_given(self):
        """Assert that ValueError is correctly raised when no lattice is provided"""
        _handler = BraggEdgeCalculator(structure_name = "BCC")
        self.assertRaises(ValueError, _handler.calculate_bragg_edges)

    def test_d_spacing_for_first_hkl_of_bcc(self):
        """Assert the d_spacing values for the first BCC structure are correct"""
        _handler = BraggEdgeCalculator(structure_name = "BCC", lattice=1.)
        _handler.calculate_hkl()
        _handler.calculate_bragg_edges()
        self.assertAlmostEqual(0.7071, _handler.d_spacing[0], delta=0.0001)
        self.assertAlmostEqual(0.5, _handler.d_spacing[1], delta=0.0001)
        self.assertAlmostEqual(0.4083, _handler.d_spacing[2], delta=0.0001)

    def test_bragg_edge_for_first_hkl_of_bcc(self):
        """Assert the bragg edge values for the first BCC structure are correct"""
        _handler = BraggEdgeCalculator(structure_name = "BCC", lattice=1.)
        _handler.calculate_hkl()
        _handler.calculate_bragg_edges()
        self.assertAlmostEqual(1.4142, _handler.bragg_edges[0], delta=0.0001)
        self.assertAlmostEqual(1.0, _handler.bragg_edges[1], delta=0.0001)
        self.assertAlmostEqual(0.8165, _handler.bragg_edges[2], delta=0.0001)

    def test_d_spacing_for_first_hkl_of_fcc(self):
        """Assert the d_spacing values for the first FCC structure are correct"""
        _handler = BraggEdgeCalculator(structure_name = "FCC", lattice=1.)
        _handler.calculate_hkl()
        _handler.calculate_bragg_edges()
        self.assertAlmostEqual(1.1547/2., _handler.d_spacing[0], delta=0.0001)
        self.assertAlmostEqual(1.0/2., _handler.d_spacing[1], delta=0.0001)
        self.assertAlmostEqual(0.7071/2., _handler.d_spacing[2], delta=0.0001)

    #def test_bragg_edge_for_first_hkl_of_fcc(self):
        #"""Assert the bragg edge values for the first FCC structure are correct"""
        #_handler = BraggEdgeCalculator(structure_name = "FCC", lattice=1.)
        #_handler.calculate_hkl()
        #_handler.calculate_bragg_edges()
        #self.assertAlmostEqual(1.1547, _handler.bragg_edges[0], delta=0.0001)
        #self.assertAlmostEqual(1.0, _handler.bragg_edges[1], delta=0.0001)
        #self.assertAlmostEqual(0.7071, _handler.bragg_edges[2], delta=0.0001)

    #def test_bragg_edge_calculate_exp_lattice(self):
        #"""Assert braggedge_calculator - experimental lattice correctly calculated"""
        #_handler = BraggEdgeCalculator(structure_name = "FCC", lattice=1.)
        #_handler.calculate_hkl()
        #_bragg_edge_exp_value = np.array([4.15297, 3.59671, 2.54284, 2.16852])
        #_bragg_edge_exp_error = np.array([0.00017, 0.00010, 0.00008, 0.00007])
        #_handler.calculate_lattice_array(_bragg_edge_exp_value, _bragg_edge_exp_error)
        #_lattice_exp = _handler.lattice_experimental
        #_expected_value = np.array([3.59658, 3.59671, 3.59612, 3.755987])
        #self.assertAlmostEqual(_expected_value[0], _lattice_exp[0], delta=0.00001)
        #self.assertAlmostEqual(_expected_value[1], _lattice_exp[1], delta=0.00001)
        #self.assertAlmostEqual(_expected_value[2], _lattice_exp[2], delta=0.00001)
        #self.assertAlmostEqual(_expected_value[3], _lattice_exp[3], delta=0.00001)
        #_expected_error = np.array([0.00015, 0.0001, 0.000113, 0.00012])
        #_lattice_error = _handler.lattice_error_experimental
        #self.assertAlmostEqual(_expected_error[0], _lattice_error[0], delta=0.00001)
        #self.assertAlmostEqual(_expected_error[1], _lattice_error[1], delta=0.00001)
        #self.assertAlmostEqual(_expected_error[2], _lattice_error[2], delta=0.00001)
        #self.assertAlmostEqual(_expected_error[3], _lattice_error[3], delta=0.00001)

if __name__ == '__main__':
    unittest.main()
