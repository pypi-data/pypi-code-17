import unittest
import os
from neutronbraggedge.braggedges_handler.structure_handler import StructureHandler
from neutronbraggedge.braggedges_handler.structure_handler import FCCHandler


class TestBraggEdgesHandler(unittest.TestCase):

    def setUp(self):
        pass

    def test_calling_with_wrong_structure(self):
        """checking that calling an unknown structure raises an error"""
        self.assertRaises(ValueError, StructureHandler, "HCC")
        
    def test_getting_the_right_first_hkl_for_BCC(self):
        """assert that the first h,k,l values are correct"""
        _handler = StructureHandler("BCC", 1)
        _list_hkl = _handler.hkl 
        self.assertEqual([1, 1, 0], _list_hkl[0])

    def test_getting_the_right_amount_of_hkl_for_BCC(self):
        """assert that the right number of hkl set is returned for BCC"""
        _handler = StructureHandler("BCC", 10)
        _list_hkl = _handler.hkl
        _nbr_hkl = len(_list_hkl)
        self.assertEqual(10, _nbr_hkl)
        
    def test_getting_the_right_first_hkl_value_for_BCC(self):
        """assert that the first few hkl set calculated are correct for BCC"""
        _handler = StructureHandler("BCC", 10)
        _list_hkl = _handler.hkl
        _nbr_hkl = len(_list_hkl)
        self.assertEqual([2, 0, 0], _list_hkl[1])
        self.assertEqual([2, 1, 1], _list_hkl[2])
        self.assertEqual([2, 2, 0], _list_hkl[3])
        self.assertEqual([2, 2, 2], _list_hkl[4])
        
    def test_getting_the_right_amount_of_hkl_for_FCC(self):
        """assert that the right number of hkl set is returned for FCC"""
        _handler = StructureHandler("FCC", 10)
        _list_hkl = _handler.hkl
        _nbr_hkl = len(_list_hkl)
        self.assertEqual(10, _nbr_hkl)
        
    def test_getting_the_right_first_hkl_value_for_FCC(self):
        """assert that the first few hkl set calculated are correct for FCC"""
        _handler = StructureHandler("FCC", 10)
        _list_hkl = _handler.hkl
        _nbr_hkl = len(_list_hkl)
        self.assertEqual([1, 1, 1], _list_hkl[0])
        self.assertEqual([2, 0, 0], _list_hkl[1])
        self.assertEqual([2, 2, 0], _list_hkl[2])
        self.assertEqual([2, 2, 2], _list_hkl[3])
        self.assertEqual([3, 1, 1], _list_hkl[4])
        
    def test_is_even_algorith(self):
        """assert that is_even algorithm is correct"""
        _fcc = FCCHandler(10)
        _is_even = _fcc._is_even(0)
        self.assertTrue(_is_even)
        _is_even = _fcc._is_even(1)
        self.assertFalse(_is_even)
        
    def test_same_parity_algorithm(self):
        """assert that same_parity algorithm is correct"""
        _fcc = FCCHandler(10)
        _same_parity = _fcc._same_parity(1, 1, 1)
        self.assertTrue(_same_parity)
        _same_parity = _fcc._same_parity(1, 1, 2)
        self.assertFalse(_same_parity)
        
        
if __name__ == '__main__':
    unittest.main()
