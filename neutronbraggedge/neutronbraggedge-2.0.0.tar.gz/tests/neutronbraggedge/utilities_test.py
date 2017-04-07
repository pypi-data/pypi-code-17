import unittest
import os
import numpy as np
from neutronbraggedge.utilities import Utilities


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data'))

    def get_full_path(self, file_name):
        return os.path.join(self.data_path, file_name)

    def test_convert_time_units_raise_value_error_when_no_data_provided(self):
        """Assert in utilities - ValueError raised when no data provided"""
        self.assertRaises(ValueError, Utilities.convert_time_units)
    
    def test_convert_time_units_raise_value_error_when_units_not_supported(self):
        """Assert in utilities - ValueError raised when no units converted"""
        self.assertRaises(ValueError, Utilities.convert_time_units, 45, 'bad_units', 's')
        self.assertRaises(ValueError, Utilities.convert_time_units, 45, 's', 'bad_units')
        self.assertRaises(ValueError, Utilities.convert_time_units, 45, 'bad_units', 'bad_units')

    def test_get_time_conversion_coeff(self):
        """Assert in utilities - correct time coefficient are returned"""
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 's', 
                                                                to_units = 's'))
        self.assertEqual(1.e3, Utilities.get_time_conversion_coeff(from_units = 's',
                                                                   to_units = 'ms'))
        self.assertEqual(1.e6, Utilities.get_time_conversion_coeff(from_units = 's',
                                                                   to_units = 'micros'))
        self.assertEqual(1.e9, Utilities.get_time_conversion_coeff(from_units = 's',
                                                                   to_units = 'ns'))
        
        self.assertEqual(1.e-3, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                   to_units = 's'))
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                to_units = 'ms'))
        self.assertEqual(1e3, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                to_units = 'micros'))
        self.assertEqual(1e6, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                to_units = 'ns'))

        self.assertEqual(1.e-6, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                   to_units = 's'))
        self.assertEqual(1.e-3, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                to_units = 'ms'))
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                to_units = 'micros'))
        self.assertEqual(1e3, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                to_units = 'ns'))

        self.assertEqual(1e-9, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 's'))
        self.assertEqual(1e-6, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 'ms'))
        self.assertEqual(1e-3, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 'micros'))
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 'ns'))
        
    def test_get_time_conversion_raise_error(self):
        """Assert in utilities - ValueError is raised when wrong units given"""
        self.assertRaises(ValueError, Utilities.get_time_conversion_coeff, 's', 'bad_units')
        self.assertRaises(ValueError, Utilities.get_time_conversion_coeff, 'bad_units', 's')
        self.assertRaises(ValueError, Utilities.get_time_conversion_coeff, 'bad_units', 'bad_units')


    def test_convert_time_units_single_value(self):
        """Assert in utilities - converting single time units value"""
        self.assertEqual(5, Utilities.convert_time_units(data = 5,
                                                         from_units = 's',
                                                         to_units = 's'))
        self.assertAlmostEqual(4.5e-3, Utilities.convert_time_units(data = 4500.,
                                                         from_units = 'micros',
                                                         to_units = 's'),
                               delta = 0.000000001)
        
    def test_convert_time_units_list_array(self):
        """Assert in utilities - converting list time units value"""
        _data = [1, 2, 3, 4, 5]
        self.assertTrue(all(_data == Utilities.convert_time_units(data = _data,
                                                             from_units = 's',
                                                             to_units = 's')))
        
    def tets_convert_time_units_numpy_array(self):
        """Assert in utilities - converting numpy array time units value"""
        _data = np.array([1., 2., 3., 4., 5.])
        self.assertTrue(all(_data == Utilities.convert_time_units(data = _data,
                                                             from_units = 's',
                                                             to_units = 's')))
        
    def test_array_multiply_coeff_with_no_array(self):
        """Assert in utilities - multiply nothing by a coeff value"""
        self.assertRaises(ValueError, Utilities.array_multiply_coeff)

    def test_array_multiply_coeff(self):
        """Assert in utilities - multiply array by coeff value"""
        _data = np.array([1., 2., 3., 4., 5.])
        _coeff = 2.5
        _new_data = Utilities.array_multiply_coeff( data = _data, 
                                                    coeff = _coeff)
        _expected_data = np.array([2.5, 5., 7.5, 10, 12.5]) 
        self.assertTrue(all(_expected_data == _new_data))   

    def test_array_add_coeff_with_no_array(self):
        """Assert in utilities - add nothing to a coeff value"""
        self.assertRaises(ValueError, Utilities.array_add_coeff)

    def test_array_add_coeff(self):
        """Assert in utilities - adding coeff to array"""
        _data = np.array([1., 2., 3., 4., 5.])
        _coeff = 5.
        _new_data = Utilities.array_add_coeff( data = _data, 
                                               coeff = _coeff)
        _expected_data = np.array([6., 7., 8., 9., 10.])
        self.assertTrue(all(_expected_data == _new_data))
        
    def test_array_divide_array_not_same_size(self):
        """Assert in Utilities - Numerator array not same size as denominator array"""
        _numerator = np.array([1, 2, 3])
        _denominator = np.array([1, 2])
        self.assertRaises(ValueError, Utilities.array_divide_array, _numerator, _denominator)
    
    def test_array_divide_array_works(self):
        """Assert in Utilities - Ratio of arrays works"""
        _numerator = np.array([10, 20, 30, 40, 50])
        _denominator = np.array([1, 2, 3, 4, 5])
        _ratio_expected = np.array([10, 10, 10, 10, 10])
        _ratio_returned = Utilities.array_divide_array(numerator = _numerator,
                                                       denominator = _denominator)
        self.assertTrue(all(_ratio_expected == _ratio_returned))
        
    def test_array_minus_array_raise_error(self):
        """Assert in Utilities - array1 minus array2 raise error if not same size"""
        _array1 = np.array([1, 2, 3])
        _array2 = np.array([1, 2])
        self.assertRaises(ValueError, Utilities.array_minus_array, _array1, _array2)
        
    def test_array_minus_array_works(self):
        """Assert in Utilities - array1 minus array2 works returns correct array"""
        _array1 = np.array([2, 4, 6])
        _array2 = np.array([2, 3, 4])
        _array_returned = Utilities.array_minus_array(_array1, _array2)
        _array_expected = np.array([0, 1, 2])
        self.assertTrue(all(_array_expected == _array_returned))

    def test_load_csv_raise_value_error(self):
        """Assert in Utilities - testing load_csv - ValueError raised when wrong file format"""
        input_file = self.get_full_path('bad_file.txt')
        self.assertRaises(ValueError, Utilities.load_csv, input_file)

    def test_load_ascii_raise_value_error(self):
        """Assert in Utilities - testing load_ascii - ValueError is raised when file format is wrong"""
        input_file = self.get_full_path('bad_file.txt')
        self.assertRaises(ValueError, Utilities.load_ascii, input_file)

    def test_load_ascii_with_space_separator(self):
        """Assert in Utilities - testing load_ascii - space separated file read correctly"""
        input_file = self.get_full_path('good_tof.txt')
        _array = Utilities.load_ascii(filename = input_file,
                                      sep = ' ')[0]
        expected_start_of_array = np.array([[1., 20.],[2., 21.]])[0]
        returned_array = _array[0:2]
        self.assertTrue(all(expected_start_of_array == returned_array))

        
if __name__ == '__main__':
    unittest.main()
