import unittest
import os
import numpy as np
from neutronbraggedge.experiment_handler.tof import TOF


class TofTest(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../data'))
    
    def get_full_path(self, file_name):
        return os.path.join(self.data_path, file_name)

    def test_loading_manual_tof_in_s_units(self):
        """Assert in TOF - TOF(s) array is correctly manually loaded"""
        _tof_array = [1., 2., 3., 4., 5., 6., 7., 8., 9.]
        _tof_handler = TOF(tof_array = _tof_array)
        self.assertTrue(all(_tof_array == _tof_handler.tof_array))

    def test_loading_manual_tof_raise_error_if_no_data_provided(self):
        """Assert in TOF - that ValueError is raised if not tof array provided"""
        self.assertRaises(ValueError, TOF)
        
    def test_loading_file_raise_error_if_file_does_not_exist(self):
        """Assert in TOF - that IOError is raised when file does not exist"""
        _filename = self.get_full_path('fake_tof.txt')
        self.assertRaises(IOError, TOF, _filename)

    def test_loading_manual_tof_in_micros_units(self):
        """Assert in TOF - TOF(micros) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.e6, 2.e6, 3.e6, 4.e6, 5.e6, 6.e6, 7.e6, 8.e6, 9.e6])
        _tof_units = 'micros'
        _tof_handler = TOF(tof_array = _tof_array, units = _tof_units)
        self.assertTrue(all(_tof_array*1.e-6 == _tof_handler.tof_array))
        
    def test_loading_manual_tof_in_ms_units(self):
        """Assert in TOF - TOF(ms) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.e3, 2.e3, 3.e3, 4.e3, 5.e3, 6.e3, 7.e3, 8.e3, 9.e3])
        _tof_units = 'ms'
        _tof_handler = TOF(tof_array = _tof_array, units = _tof_units)
        self.assertTrue(all(_tof_array*1.e-3 == _tof_handler.tof_array))

    def test_loading_manual_tof_in_ns_units(self):
        """Assert in TOF - TOF(ms) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.e9, 2.e9, 3.e9, 4.e9, 5.e9, 6.e9, 7.e9, 8.e9, 9.e9])
        _tof_units = 'ns'
        _tof_handler = TOF(tof_array = _tof_array, units = _tof_units)
        self.assertTrue(all(_tof_array*1.e-9 == _tof_handler.tof_array))

    def test_loading_manual_tof_units_not_implemented_yet(self):
        """Assert in TOF - that an error is thrown when the units is not recognized"""
        _tof_array = np.array([1.e9, 2.e9, 3.e9, 4.e9, 5.e9, 6.e9, 7.e9, 8.e9, 9.e9])
        _tof_units = 'crazys'
        self.assertRaises(NotImplementedError, None, TOF, _tof_array, _tof_units)

    def test_loading_good_tof_file(self):
        """Assert in TOF - that correctly formated tof file is correctly loaded"""
        _filename = self.get_full_path('good_tof.txt')
        _tof_handler = TOF(filename = _filename)
        _tof_expected = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertTrue(all(_tof_expected == _tof_handler.tof_array[0:4]))

    def test_loading_real_tof_file(self):
        """Assert in TOF - that real tof file is correctly loaded"""
        _filename = self.get_full_path('tof.txt')
        _tof_handler = TOF(filename = _filename)
        _tof_expected = np.array([9.6e-7, 1.12e-5, 2.144e-5, 3.168e-5])
        self.assertTrue(all(_tof_expected == _tof_handler.tof_array[0:4]))
        
    def test_loading_counts_column(self):
        """Assert in TOF - second column (counts) is correctly loaded"""
        _filename = self.get_full_path('tof.txt')
        _tof_handler = TOF(filename = _filename)
        _counts_expected = np.array([2137, 1988, 1979, 2078])
        self.assertTrue(all(_counts_expected == _tof_handler.counts_array[0:4]))


if __name__ == '__main__':
    unittest.main()
